# Golden-Sun-Spritesheet-Compressor
For format #0 of GS sprites.

## How to use:
Arguments are not command-line. You need to have Python installed.

Edit the variables at the top:
```
input_folder = Your folder name. It should be a folder of .pngs, labelled in order. Follows aseprite .png export, so e.g. Isaac1.png, Isaac2.png...
output_spritesheet_name = Outputs spritesheet data
output_pointers_name = Outputs pointer data
starting_pointer = 0x806D40 Start of pointers. This is where the spritesheet data is inserted.
```

To insert (manual hex editing), replace all the sprite pointers with pointer data, and insert the spritesheet data where you defined the starting_pointer. 
**Make sure to change your character's sprite type to format 0.**

Then run the program in command line. Maybe I'll add command line args support in the future.

# Special Thanks
Salanewt, Beyond, and tarpman from the GS Hacking server 
Atrius for TLAEditor (so I can double check if I did things right)
