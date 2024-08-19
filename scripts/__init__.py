from .unet_loader import register_unet_loader

def on_app_started(demo, app):
    register_unet_loader()
