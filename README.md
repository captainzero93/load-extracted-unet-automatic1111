# Safetensor UNet Loader / Merge Plugin for AUTOMATIC1111 Stable Diffusion Web UI

This extension for AUTOMATIC1111's Stable Diffusion Web UI allows you to use separate UNet and non-UNet parts of Stable Diffusion models. It's designed to save space and give you more flexibility in managing your models.

## What Does This Plugin Do?

This plugin lets you:
1. Load separate UNet and non-UNet parts of a Stable Diffusion model.
2. Combine these parts into a full model that you can use for generating images.
3. Save space on your computer by reusing the non-UNet parts with different UNets.

## Why Should I Use This?

1. **Save Space**: Instead of storing many full models, you can store one non-UNet part and multiple UNet parts, saving gigabytes of space.
2. **More Models, Less Storage**: You can have more model variations without using as much storage space.
3. **Future-Ready**: As models get bigger and more complex, this approach will become even more helpful for managing storage.

## How to Install

1. Open your AUTOMATIC1111 Stable Diffusion Web UI folder.
2. Find the `extensions` folder inside it.
3. Open a command prompt or terminal in this folder.
4. Run this command:
   ```
   git clone https://github.com/captainzero93/load-extracted-unet-automatic1111.git
   ```
5. Restart your AUTOMATIC1111 Stable Diffusion Web UI.

## How to Use

1. First, you need to split your Stable Diffusion models into UNet and non-UNet parts. Use the [UNet Extractor and Remover tool](https://github.com/captainzero93/extract-unet-safetensor) for this.
2. After splitting, you'll have two files for each model: a UNet file and a non-UNet file.
3. Put these files in the `extensions/load-extracted-unet-automatic1111/models` folder.
4. Start (or restart) your AUTOMATIC1111 Stable Diffusion Web UI.
5. In the Web UI, look for the "UNet Loader" tab.
6. In this tab:
   - Choose a UNet file from the "UNet File" dropdown.
   - Choose a non-UNet file from the "Non-UNet File" dropdown.
   - Click "Load Model Parts".
7. The plugin will combine these parts into a full model.
8. **Important**: Wait for the extension output box to display "UNet and non-UNet parts combined and loaded successfully." This indicates that the model is ready to use, even if the UI doesn't show the loaded model name.
9. You can now use this combined model in the txt2img and img2img tabs just like any other model.

## Important Notes

- This plugin works best with files created by the [UNet Extractor and Remover tool](https://github.com/captainzero93/extract-unet-safetensor).
- Make sure your computer (especially your GPU) has enough memory to handle the combined model.
- If things seem slow, try restarting the Web UI to clear the memory.
- The UI may not always show the loaded model name, but this doesn't affect functionality. Always refer to the extension output box for confirmation.
- The extension creates temporary combined model files. Use the "Cleanup Last Combined Model" button to remove these when you're done.

## Troubleshooting

If you have problems:
1. Check that your files are in the correct folder (`extensions/load-extracted-unet-automatic1111/models`).
2. Make sure you're using files created by the UNet Extractor tool.
3. Look at the console output and the extension output box for error messages or success confirmation.
4. If the UI doesn't show the loaded model, but the output box confirms it's loaded, proceed with generation anyway.
5. Try refreshing the file list using the "Refresh File List" button if new files aren't appearing.
6. If it's still not working, try restarting the Web UI.
7. Ensure you have enough VRAM for the combined model. If you're getting out-of-memory errors, try using a smaller model or freeing up GPU resources.

## Recent Updates

- Added dynamic model directory detection for better compatibility with different installation methods.
- Improved error handling and logging for easier troubleshooting.
- Added a "Refresh File List" button to update the file dropdowns without restarting.
- Implemented a model cache to speed up loading of previously combined models.

## Getting Help

If you're stuck, you can:
1. Check the [issues page](https://github.com/captainzero93/load-extracted-unet-automatic1111/issues) to see if others have had the same problem.
2. Create a new issue if your problem isn't already listed. When reporting issues, please include:
   - The exact steps you took
   - Any error messages from the console or extension output box
   - Your system specifications (OS, GPU, VRAM)

## Legal Stuff

This plugin is free to use, modify, and share. However, if you use it in your own project, please include this credit:

```
Original work: https://github.com/captainzero93/load-extracted-unet-automatic1111
```

See the [LICENSE](LICENSE) file for full legal details.

## Thank You

- To everyone who uses and supports this plugin.
- To the AUTOMATIC1111 Stable Diffusion Web UI community.
- To all contributors who help improve this project.
