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
8. You can now use this combined model in the txt2img and img2img tabs just like any other model.

## Important Notes

- This plugin works best with files created by the [UNet Extractor and Remover tool](https://github.com/captainzero93/extract-unet-safetensor).
- Make sure your computer (especially your GPU) has enough memory to handle the combined model.
- If things seem slow, try restarting the Web UI to clear the memory.

## Troubleshooting

If you have problems:
1. Check that your files are in the correct folder.
2. Make sure you're using files created by the UNet Extractor tool.
3. Look at the console output for error messages.
4. If it's still not working, try restarting the Web UI.

## Getting Help

If you're stuck, you can:
1. Check the [issues page](https://github.com/captainzero93/load-extracted-unet-automatic1111/issues) to see if others have had the same problem.
2. Create a new issue if your problem isn't already listed.

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
