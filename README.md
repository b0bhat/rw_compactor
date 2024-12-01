A fast, customizable and multithreaded script which resizes too-large textures in mods to prevent crash during load while stitching texture atlas.
- When rimworld is loading with many (500+) mods, unity's texture atlas stitching tends to OOM, especially when some mods have textures which are far larger than required.
- Some especially egregious mods have 100mb+ textures which can be resized to less than 5% of it's original size and still retain graphical fidelity.
- Unfortunately, Steam will validate and re-download the original files of all your mods when new mods are added, and this script needs to be re-run.
