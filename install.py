import launch

print("UNet Loader install script is running")

if not launch.is_installed("safetensors"):
    launch.run_pip("install safetensors", "requirements for UNet Loader")

if not launch.is_installed("torch"):
    launch.run_pip("install torch", "requirements for UNet Loader")

if not launch.is_installed("asyncio"):
    launch.run_pip("install asyncio", "requirements for UNet Loader")

print("UNet Loader extension installed successfully.")
