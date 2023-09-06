from PIL import Image
import numpy as np
import math
import os 

charname = "isaac"
gamename = "TBS"



input_folder = f"input_{charname}_{gamename}" #folder of .pngs go here
output_spritesheet_name = f"{charname}_{gamename}_spritesheet.bin"
output_pointers_name = f"{charname}_{gamename}_pointers.bin"
starting_pointer = 0x08007C70  #where the spritesheet will be inserted in data. PLEASE REMEMBER THE 08

def convert_png_to_bgr555(input_file, output_file = None):
    # Open the PNG image using PIL (Python Imaging Library)
    image = Image.open(input_file)

    # Convert the image to RGB mode if it's not already
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Get the image dimensions
    width, height = image.size

    # Convert the image to a NumPy array for efficient manipulation
    pixel_data = np.array(image)

    # Convert RGB888 to BGR555
    bgr555_data = ((pixel_data[:, :, 2] >> 3) << 10) | ((pixel_data[:, :, 1] >> 3) << 5) | (pixel_data[:, :, 0] >> 3)


    # Convert the NumPy array to bytes
    bgr555_bytes = bgr555_data.astype(np.uint16).tobytes()
    
    pixel_size = 2  # 2 bytes per pixel
    pixel_count = len(bgr555_bytes) // pixel_size
    pixels = [bgr555_bytes[i * pixel_size:(i + 1) * pixel_size] for i in range(pixel_count)]

    return pixels

def distance(a, b):
    return math.hypot(*(v2 - v1 for v1, v2 in zip(a, b)))


def create_test_palette(data):
    squareSide = 15
    imgdata = np.zeros((squareSide, squareSide, 4), dtype = np.uint8)
    for col in range(squareSide):
        for row in range(squareSide):
            if (row*squareSide + col) >= len(data):
                imgdata[row][col] = (0, 0, 0, 0)
            else:
                imgdata[row][col] = data[row * squareSide + col]
    img = Image.fromarray(imgdata)
    img.show()
    
def create_test_image(data, inv_palette): #GUESS WHAT. IT WORKS.
    imgdata = np.zeros((32, 32, 4), dtype = np.uint8)
    index = 0
    imgindex = 0
     
    
    while True: 
        byte = int.from_bytes(data[index], 'little')
        
        if byte == 0:
            break 
        if byte < 0xE0: 
            imgdata[imgindex//32, imgindex%32] = inv_palette[data[index]]
            imgindex += 1
        else: 
            imgindex += byte - 0xDF
        
        index += 1

        
    img = Image.fromarray(imgdata)
    img.show()


def encode_image_with_palette(data, palette_array, palette_dict, output_file = None):
    encoded_data = bytearray()
    current_color = None
    transparency_count = 0
    lastColorIsTransparent = False
    #print(data)
    for pixel in data:
        #print(pixel)
        if pixel[3] == 0:  # Transparency
            transparency_count += 1
            lastColorIsTransparent = True
            
        else:
            lastColorIsTransparent = False

            current_color = palette_dict.get(pixel)
            #print(current_color)
            #print(pixel)
            if current_color is None:
            
                current_color = common_colors.get(pixel)
                
                if current_color is None:
                #print(f"Color {pixel} not found in the palette_dict.")
                    closest = sorted(palette_array, key=lambda x: distance(pixel, x))[0]
                    #print(f"Closest: {closest}")

                    #print(f"Closest color: {closest}")
                    current_color = palette_dict.get(closest)
                    common_colors[pixel] = current_color
                    #print(common_colors)
                
            #print(f"Final color: {current_color.hex()} / {int.from_bytes(current_color, 'little')}")
            #print("--")
            
            if current_color is not None:
                if transparency_count > 0:
                    #print(transparency_count)
                    #print(f"Transparency count: {transparency_count}")

                    while transparency_count >= 0xFF - 0xDF:  # Max space
                        #print(f"appending 0xFF ({0xFF - 0xDF})")
                        
                        encoded_data.append(0xFF)
                        transparency_count -= (0xFF - 0xDF)
                        
                        #print(f"remainder: {transparency_count}")
                    
                    #print(f"final append: {transparency_count + 0xDF}")
                    #print((transparency_count + 0xDF).to_bytes(1, "little"))
                    
                    remainder = transparency_count + 0xDF
                    if remainder != 0xDF:
                        encoded_data.append(transparency_count + 0xDF)  # Add remaining space
                    transparency_count = 0
                    

                    #print("---")
                   
                encoded_data.extend(current_color)
            #print("----------")

                

    
    # Add the final color if there is one
    
    if current_color is not None:
        if lastColorIsTransparent:
            encoded_data.extend(b'\x00')
        
        else:
            if transparency_count > 0:
                while transparency_count >= 0xFF - 0xDF:
                    encoded_data.append(0xFF)
                    transparency_count -= (0xFF - 0xDF)
                encoded_data.append(transparency_count + 0xDF)
            encoded_data.extend(current_color)
    
    
    return encoded_data 
    #with open(output_file, 'wb') as file:
    #    file.write(encoded_data)  

palette_array = ['0000', '001F', '01DF', '03FF', '03E0', '1DC7', '7FE0', '7C00', '59DC', '3ADF', '01D6', '000E', '1CE7', '4E73', '7FFF', '00FF', '01DC', '0007', '02C0', '02C7', '02CE', '02D6', '02DC', '02DF', '0380', '0387', '038E', '0396', '039C', '039F', '0016', '03E7', '03EE', '03F6', '03FC', '00E7', '1C00', '1C07', '1C0E', '1C16', '1C1C', '1C1F', '1CE0', '001C', '1CEE', '1CF6', '1CFC', '1CFF', '1DC0', '01C0', '1DCE', '1DD6', '1DDC', '1DDF', '1EC0', '1EC7', '1ECE', '1ED6', '1EDC', '1EDF', '1F80', '1F87', '1F8E', '1F96', '1F9C', '1F9F', '1FE0', '1FE7', '1FEE', '1FF6', '1FFC', '1FFF', '3800', '3807', '380E', '3816', '381C', '381F', '38E0', '38E7', '38EE', '38F6', '38FC', '38FF', '39C0', '39C7', '39CE', '39D6', '39DC', '39DF', '3AC0', '3AC7', '3ACE', '3AD6', '3ADC', '00FC', '3B80', '3B87', '3B8E', '3B96', '3B9C', '3B9F', '3BE0', '3BE7', '3BEE', '3BF6', '3BFC', '3BFF', '5800', '5807', '580E', '5816', '581C', '581F', '58E0', '58E7', '58EE', '58F6', '58FC', '58FF', '59C0', '59C7', '59CE', '59D6', '00F6', '59DF', '5AC0', '5AC7', '5ACE', '5AD6', '5ADC', '5ADF', '5B80', '5B87', '5B8E', '5B96', '5B9C', '5B9F', '5BE0', '5BE7', '5BEE', '5BF6', '5BFC', '5BFF', '7000', '7007', '700E', '7016', '701C', '701F', '70E0', '70E7', '70EE', '70F6', '70FC', '70FF', '71C0', '71C7', '71CE', '71D6', '71DC', '71DF', '72C0', '72C7', '72CE', '72D6', '72DC', '72DF', '7380', '7387', '738E', '7396', '739C', '739F', '73E0', '73E7', '73EE', '73F6', '73FC', '73FF', '00E0', '7C07', '7C0E', '7C16', '7C1C', '7C1F', '7CE0', '7CE7', '7CEE', '7CF6', '7CFC', '7CFF', '7DC0', '7DC7', '7DCE', '7DD6', '7DDC', '7DDF', '7EC0', '7EC7', '7ECE', '7ED6', '7EDC', '7EDF', '7F80', '7F87', '7F8E', '7F96', '7F9C', '7F9F', '00EE', '7FE7', '7FEE', '7FF6', '7FFC', '01CE', '0C63', '14A5', '294A', '318C', '01C7', '4210', '6739']


def bgr555_to_rgba8888(value):
    blue = (value >> 10) & 0x1F
    green = (value >> 5) & 0x1F
    red = value & 0x1F
    alpha = 255  # You can set the alpha value to 255 for fully opaque pixels.
    
    # Expand from 5 bits to 8 bits per channel
    blue = (blue << 3) | (blue >> 2)
    green = (green << 3) | (green >> 2)
    red = (red << 3) | (red >> 2)
    
    return red, green, blue, alpha
#convert_png_to_bgr555("red felix1.png", "testOutput.dmp")

palette_array = [(0,0,0,0)] + [bgr555_to_rgba8888(int(i,16)) for i in palette_array]

#create_test_palette(palette_array)

#palette_dict = {}

#for i in range(0, len(palette_array)):
#    palette_dict[palette_array[i]] = i.to_bytes(1, 'little')


palette_dict = {(0, 0, 0, 0): b'\x00', (0, 0, 0, 255): b'\x01', (255, 0, 0, 255): b'\x02', (255, 115, 0, 255): b'\x03', (255, 255, 0, 255): b'\x04', (0, 255, 0, 255): b'\x05', (57, 115, 57, 255): b'\x06', (0, 255, 255, 255): b'\x07', (0, 0, 255, 255): b'\x08', (231, 115, 181, 255): b'\t', (255, 181, 115, 255): b'\n', (181, 115, 0, 255): b'\x0b', (115, 0, 0, 255): b'\x0c', (57, 57, 57, 255): b'\r', (156, 156, 156, 255): b'\x0e', (255, 255, 255, 255): b'\x0f', (255, 57, 0, 255): b'\x10', (231, 115, 0, 255): b'\x11', (57, 0, 0, 255): b'\x12', (0, 181, 0, 255): b'\x13', (57, 181, 0, 255): b'\x14', (115, 181, 0, 255): b'\x15', (181, 181, 0, 255): b'\x16', (231, 181, 0, 255): b'\x17', (255, 181, 0, 255): b'\x18', (0, 231, 0, 255): b'\x19', (57, 231, 0, 255): b'\x1a', (115, 231, 0, 255): b'\x1b', (181, 231, 0, 255): b'\x1c', (231, 231, 0, 255): b'\x1d', (255, 231, 0, 255): b'\x1e', (181, 0, 0, 255): b'\x1f', (57, 255, 0, 255): b' ', (115, 255, 0, 255): b'!', (181, 255, 0, 255): b'"', (231, 255, 0, 255): b'#', (57, 57, 0, 255): b'$', (0, 0, 57, 255): b'%', (57, 0, 57, 255): b'&', (115, 0, 57, 255): b"'", (181, 0, 57, 255): b'(', (231, 0, 57, 255): b')', (255, 0, 57, 255): b'*', (0, 57, 57, 255): b'+', (231, 0, 0, 255): b',', (115, 57, 57, 255): b'-', (181, 57, 57, 255): b'.', (231, 57, 57, 255): b'/', (255, 57, 57, 255): b'0', (0, 115, 57, 255): b'1', (0, 115, 0, 255): b'2', (115, 115, 57, 255): b'3', (181, 115, 57, 255): b'4', (231, 115, 57, 255): b'5', (255, 115, 57, 255): b'6', (0, 181, 57, 255): b'7', (57, 181, 57, 255): b'8', (115, 181, 57, 255): b'9', (181, 181, 57, 255): b':', (231, 181, 57, 255): b';', (255, 181, 57, 255): b'<', (0, 231, 57, 255): b'=', (57, 231, 57, 255): b'>', (115, 231, 57, 255): b'?', (181, 231, 57, 255): b'@', (231, 231, 57, 255): b'A', (255, 231, 57, 255): b'B', (0, 255, 57, 255): b'C', (57, 255, 57, 255): b'D', (115, 255, 57, 255): b'E', (181, 255, 57, 255): b'F', (231, 255, 57, 255): b'G', (255, 255, 57, 255): b'H', (0, 0, 115, 255): b'I', (57, 0, 115, 255): b'J', (115, 0, 115, 255): b'K', (181, 0, 115, 255): b'L', (231, 0, 115, 255): b'M', (255, 0, 115, 255): b'N', (0, 57, 115, 255): b'O', (57, 57, 115, 255): b'P', (115, 57, 115, 255): b'Q', (181, 57, 115, 255): b'R', (231, 57, 115, 255): b'S', (255, 57, 115, 255): b'T', (0, 115, 115, 255): b'U', (57, 115, 115, 255): b'V', (115, 115, 115, 255): b'W', (181, 115, 115, 255): b'X', (231, 115, 115, 255): b'Y', (255, 115, 115, 255): b'Z', (0, 181, 115, 255): b'[', (57, 181, 115, 255): b'\\', (115, 181, 115, 255): b']', (181, 181, 115, 255): b'^', (231, 181, 115, 255): b'_', (231, 57, 0, 255): b'`', (0, 231, 115, 255): b'a', (57, 231, 115, 255): b'b', (115, 231, 115, 255): b'c', (181, 231, 115, 255): b'd', (231, 231, 115, 255): b'e', (255, 231, 115, 255): b'f', (0, 255, 115, 255): b'g', (57, 255, 115, 255): b'h', (115, 255, 115, 255): b'i', (181, 255, 115, 255): b'j', (231, 255, 115, 255): b'k', (255, 255, 115, 255): b'l', (0, 0, 181, 255): b'm', (57, 0, 181, 255): b'n', (115, 0, 181, 255): b'o', (181, 0, 181, 255): b'p', (231, 0, 181, 255): b'q', (255, 0, 181, 255): b'r', (0, 57, 181, 255): b's', (57, 57, 181, 255): b't', (115, 57, 181, 255): b'u', (181, 57, 181, 255): b'v', (231, 57, 181, 255): b'w', (255, 57, 181, 255): b'x', (0, 115, 181, 255): b'y', (57, 115, 181, 255): b'z', (115, 115, 181, 255): b'{', (181, 115, 181, 255): b'|', (181, 57, 0, 255): b'}', (255, 115, 181, 255): b'~', (0, 181, 181, 255): b'\x7f', (57, 181, 181, 255): b'\x80', (115, 181, 181, 255): b'\x81', (181, 181, 181, 255): b'\x82', (231, 181, 181, 255): b'\x83', (255, 181, 181, 255): b'\x84', (0, 231, 181, 255): b'\x85', (57, 231, 181, 255): b'\x86', (115, 231, 181, 255): b'\x87', (181, 231, 181, 255): b'\x88', (231, 231, 181, 255): b'\x89', (255, 231, 181, 255): b'\x8a', (0, 255, 181, 255): b'\x8b', (57, 255, 181, 255): b'\x8c', (115, 255, 181, 255): b'\x8d', (181, 255, 181, 255): b'\x8e', (231, 255, 181, 255): b'\x8f', (255, 255, 181, 255): b'\x90', (0, 0, 231, 255): b'\x91', (57, 0, 231, 255): b'\x92', (115, 0, 231, 255): b'\x93', (181, 0, 231, 255): b'\x94', (231, 0, 231, 255): b'\x95', (255, 0, 231, 255): b'\x96', (0, 57, 231, 255): b'\x97', (57, 57, 231, 255): b'\x98', (115, 57, 231, 255): b'\x99', (181, 57, 231, 255): b'\x9a', (231, 57, 231, 255): b'\x9b', (255, 57, 231, 255): b'\x9c', (0, 115, 231, 255): b'\x9d', (57, 115, 231, 255): b'\x9e', (115, 115, 231, 255): b'\x9f', (181, 115, 231, 255): b'\xa0', (231, 115, 231, 255): b'\xa1', (255, 115, 231, 255): b'\xa2', (0, 181, 231, 255): b'\xa3', (57, 181, 231, 255): b'\xa4', (115, 181, 231, 255): b'\xa5', (181, 181, 231, 255): b'\xa6', (231, 181, 231, 255): b'\xa7', (255, 181, 231, 255): b'\xa8', (0, 231, 231, 255): b'\xa9', (57, 231, 231, 255): b'\xaa', (115, 231, 231, 255): b'\xab', (181, 231, 231, 255): b'\xac', (231, 231, 231, 255): b'\xad', (255, 231, 231, 255): b'\xae', (0, 255, 231, 255): b'\xaf', (57, 255, 231, 255): b'\xb0', (115, 255, 231, 255): b'\xb1', (181, 255, 231, 255): b'\xb2', (231, 255, 231, 255): b'\xb3', (255, 255, 231, 255): b'\xb4', (0, 57, 0, 255): b'\xb5', (57, 0, 255, 255): b'\xb6', (115, 0, 255, 255): b'\xb7', (181, 0, 255, 255): b'\xb8', (231, 0, 255, 255): b'\xb9', (255, 0, 255, 255): b'\xba', (0, 57, 255, 255): b'\xbb', (57, 57, 255, 255): b'\xbc', (115, 57, 255, 255): b'\xbd', (181, 57, 255, 255): b'\xbe', (231, 57, 255, 255): b'\xbf', (255, 57, 255, 255): b'\xc0', (0, 115, 255, 255): b'\xc1', (57, 115, 255, 255): b'\xc2', (115, 115, 255, 255): b'\xc3', (181, 115, 255, 255): b'\xc4', (231, 115, 255, 255): b'\xc5', (255, 115, 255, 255): b'\xc6', (0, 181, 255, 255): b'\xc7', (57, 181, 255, 255): b'\xc8', (115, 181, 255, 255): b'\xc9', (181, 181, 255, 255): b'\xca', (231, 181, 255, 255): b'\xcb', (255, 181, 255, 255): b'\xcc', (0, 231, 255, 255): b'\xcd', (57, 231, 255, 255): b'\xce', (115, 231, 255, 255): b'\xcf', (181, 231, 255, 255): b'\xd0', (231, 231, 255, 255): b'\xd1', (255, 231, 255, 255): b'\xd2', (115, 57, 0, 255): b'\xd3', (57, 255, 255, 255): b'\xd4', (115, 255, 255, 255): b'\xd5', (181, 255, 255, 255): b'\xd6', (231, 255, 255, 255): b'\xd7', (115, 115, 0, 255): b'\xd8', (24, 24, 24, 255): b'\xd9', (41, 41, 41, 255): b'\xda', (82, 82, 82, 255): b'\xdb', (99, 99, 99, 255): b'\xdc', (57, 115, 0, 255): b'\xdd', (132, 132, 132, 255): b'\xde', (206, 206, 206, 255): b'\xdf'}


inv_palette = {v: k for k, v in palette_dict.items()}


global common_colors
common_colors = {}


cwd = os.getcwd()
folder_path = os.path.join(cwd, input_folder)
files = os.listdir(folder_path)


files.sort(key = lambda x:int(''.join(str(c) for c in x if c.isdigit())))


pointer_output = bytearray()
output = bytearray()


pointer = starting_pointer
pointer_output.extend(pointer.to_bytes(4, byteorder = 'little'))

for filename in files:

    image = Image.open(os.path.join(folder_path, filename)).convert("RGBA")
    print(filename)
    imageArray = []
    for row in np.array(image):
        for col in row:
            imageArray.append(tuple(col))

            
    imageData = encode_image_with_palette(imageArray, palette_array, palette_dict) 
    
    output += imageData 
    pointer += len(imageData)
    pointer_output.extend(pointer.to_bytes(4, byteorder = 'little'))
    


with open(output_spritesheet_name, 'wb') as file:
    file.write(output)  
    
with open(output_pointers_name, 'wb') as file:
    file.write(pointer_output[:-4])

