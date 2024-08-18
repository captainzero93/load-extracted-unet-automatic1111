import os
import torch
from modules import shared, devices, sd_models, script_callbacks, sd_hijack
from safetensors.torch import load_file, save_file
import gradio as gr
from collections import OrderedDict
import asyncio
import gc

class ModelCache:
    def __init__(self, max_size=3):
        self.cache = OrderedDict()
        self.max_size = max_size

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return None

    def set(self, key, model):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.max_size:
            _, old_model = self.cache.popitem(last=False)
            old_model.to('cpu')
            torch.cuda.empty_cache()
        self.cache[key] = model

model_cache = ModelCache()
last_combined_model_path = None

def get_safetensors_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.safetensors')]

async def load_file_async(file_path, device='cpu'):
    return await asyncio.to_thread(load_file, file_path, device)

async def load_unet_and_non_unet(unet_file, non_unet_file):
    global last_combined_model_path
    models_dir = os.path.join(shared.script_path, "extensions", "unet_loader_extension", "models")
    unet_path = os.path.join(models_dir, unet_file)
    non_unet_path = os.path.join(models_dir, non_unet_file)

    try:
        print(f"Attempting to load UNet file: {unet_path}")
        print(f"Attempting to load non-UNet file: {non_unet_path}")

        if not os.path.exists(unet_path) or not os.path.exists(non_unet_path):
            return "Error: One or both files do not exist. Please check the file paths."

        cache_key = (unet_path, non_unet_path)
        cached_model = model_cache.get(cache_key)
        if cached_model is not None:
            print("Loading model from cache")
            shared.sd_model = cached_model
            shared.sd_model.to(devices.device)
            return "Model loaded from cache and ready for use."

        # Load files asynchronously
        non_unet_state_dict, unet_state_dict = await asyncio.gather(
            load_file_async(non_unet_path),
            load_file_async(unet_path)
        )

        print("Files loaded successfully")

        # Combine the state dicts
        combined_state_dict = {**non_unet_state_dict, **unet_state_dict}
        print("State dictionaries combined")

        # Create a temporary combined safetensors file
        combined_model_name = f"Combined_{os.path.splitext(unet_file)[0]}_{os.path.splitext(non_unet_file)[0]}"
        combined_model_path = os.path.join(models_dir, f"{combined_model_name}.safetensors")
        save_file(combined_state_dict, combined_model_path)
        print(f"Combined model saved as {combined_model_path}")

        # Store the path of the last combined model
        last_combined_model_path = combined_model_path

        # Create a new checkpoint info
        new_checkpoint_info = sd_models.CheckpointInfo(combined_model_path)
        new_checkpoint_info.calculate_shorthash()

        # Register the new checkpoint
        sd_models.checkpoint_aliases[combined_model_name] = combined_model_path
        sd_models.checkpoints_list[new_checkpoint_info.title] = new_checkpoint_info

        # Thoroughly unload the current model and clear VRAM
        print("Unloading current model and clearing VRAM...")
        if shared.sd_model is not None:
            sd_hijack.model_hijack.undo_hijack(shared.sd_model)
            shared.sd_model = None
        
        gc.collect()
        devices.torch_gc()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
        
        print("VRAM cleared")

        # Manually load the new model
        print(f"Loading new combined model from {combined_model_path}...")
        shared.sd_model = sd_models.load_model(new_checkpoint_info)
        
        # Move model to appropriate device and optimize
        shared.sd_model.to(devices.device)
        if not shared.cmd_opts.no_half:
            shared.sd_model.half()
        shared.sd_model.eval()
        
        # Apply hijack
        sd_hijack.model_hijack.hijack(shared.sd_model)
        
        # Add to cache
        model_cache.set(cache_key, shared.sd_model)

        print(f"New combined model loaded from {combined_model_path}")

        # Update UI and shared data
        shared.opts.data["sd_model_checkpoint"] = new_checkpoint_info.title
        shared.opts.data["sd_checkpoint_hash"] = new_checkpoint_info.sha256

        # Ensure the model is set as the current model
        sd_models.model_data.set_sd_model(shared.sd_model)

        # Force UI update
        shared.state.interrupt()
        shared.state.need_reload_model = True

        return f"UNet and non-UNet parts combined and loaded successfully. The combined model '{combined_model_name}' is now the active checkpoint and ready for use in txt2img."
    except Exception as e:
        print(f"Error loading UNet and non-UNet parts: {str(e)}")
        return f"Error loading UNet and non-UNet parts: {str(e)}"

def cleanup_last_combined_model():
    global last_combined_model_path
    if last_combined_model_path and os.path.exists(last_combined_model_path):
        try:
            os.remove(last_combined_model_path)
            print(f"Removed temporary combined model: {last_combined_model_path}")
            last_combined_model_path = None
            return "Last combined model cleaned up successfully."
        except Exception as e:
            print(f"Error cleaning up last combined model: {str(e)}")
            return f"Error cleaning up last combined model: {str(e)}"
    else:
        return "No combined model to clean up or file not found."

def on_ui_tabs():
    models_dir = os.path.join(shared.script_path, "extensions", "unet_loader_extension", "models")
    os.makedirs(models_dir, exist_ok=True)
    safetensors_files = get_safetensors_files(models_dir)

    with gr.Blocks(analytics_enabled=False) as unet_loader_interface:
        gr.Markdown(
        """
        # UNet Loader
        This interface allows you to load separate UNet and non-UNet parts of a model.
        Select your .safetensors files from the dropdowns and click 'Load Model Parts'.
        Place your .safetensors files in the 'extensions/unet_loader_extension/models' folder.
        """
        )
        with gr.Row():
            unet_dropdown = gr.Dropdown(choices=safetensors_files, label="UNet File", interactive=True)
            non_unet_dropdown = gr.Dropdown(choices=safetensors_files, label="Non-UNet File", interactive=True)
        load_button = gr.Button("Load Model Parts")
        cleanup_button = gr.Button("Cleanup Last Combined Model")
        output_text = gr.Textbox(label="Output", interactive=False)

        def refresh_dropdown():
            updated_files = get_safetensors_files(models_dir)
            return gr.Dropdown.update(choices=updated_files), gr.Dropdown.update(choices=updated_files)

        refresh_button = gr.Button("Refresh File List")
        refresh_button.click(refresh_dropdown, inputs=[], outputs=[unet_dropdown, non_unet_dropdown])

        load_button.click(
            fn=lambda unet, non_unet: asyncio.run(load_unet_and_non_unet(unet, non_unet)),
            inputs=[unet_dropdown, non_unet_dropdown],
            outputs=[output_text]
        )

        cleanup_button.click(
            fn=cleanup_last_combined_model,
            inputs=[],
            outputs=[output_text]
        )

    return [(unet_loader_interface, "UNet Loader", "unet_loader_tab")]

def on_app_started(demo, app):
    pass

script_callbacks.on_ui_tabs(on_ui_tabs)
script_callbacks.on_app_started(on_app_started)

print("UNet Loader script loaded successfully")