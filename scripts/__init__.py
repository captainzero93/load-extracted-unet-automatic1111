from .unet_loader import on_app_started, on_ui_tabs
from modules import script_callbacks

print("UNet Loader __init__.py is being executed")

def initialize():
    script_callbacks.on_ui_tabs(on_ui_tabs)
    script_callbacks.on_app_started(on_app_started)

print("UNet Loader __init__.py execution completed")
