

from PIL import Image
import numpy as np
import math
import os 
import struct 

width = 64 # in denary, please 
height = 64 # in denary, please
game = "gs1.gba"

pointerTable_start = 0x2DDC74 


battle_pointer_dict = {
    "TBS" : {
        "Isaac" : 0x2DDC74,
        "Garet" : 0x2E7A1C,
        "Ivan" : 0x2F813C,
        "Mia" : 0x3000BC
    }
}
#startPointer = 0x2D8C80 #NO 08 for these
#endPointer = 0x2E1E54

def export_image_from_data(data, width, height, inv_palette): #GUESS WHAT. IT WORKS.
    imgdata = np.zeros((width, height, 4), dtype = np.uint8)
    index = 0
    imgindex = 0
     
    
    while True: 
        byte = data[index]
        
        if byte == 0:
            break 
        if byte < 0xE0: 
            
            imgdata[imgindex//width, imgindex%height] = inv_palette[byte.to_bytes(1, 'little')]
            imgindex += 1
        else: 
            imgindex += byte - 0xDF
        
        index += 1
    #img = Image.fromarray(imgdata)
    #img.show()
    return imgdata 
    #img = Image.fromarray(imgdata)
    #img.show()
def export_character(golden_sun, character, pointerTable_start, inv_palette): 
    pointer_table = golden_sun[pointerTable_start:]

    pointerTable_end = 0

    addresses = []
    for i in range(0, len(pointer_table), 4):
        pointer = [j for j in pointer_table[i:i+4]]
        result = bytearray()

        for i in pointer:
            result.extend(i.to_bytes(1, byteorder='little'))

        result = result
        address = bytes(result[:-1])
        

        if pointer[-1] != 0x08:
            break
        
        
        addresses.append(int.from_bytes(address, 'little'))



    for addressIndex in range(len(addresses)):
        address = addresses[addressIndex]
        image_data = golden_sun[address:address + width*height]
        for i in range(0, len(image_data), width*height):
            imgdata = export_image_from_data(image_data[i:i+width*height], width, height, inv_palette)
            
            Image.fromarray(imgdata).save(f"image_output/{character}{addressIndex}.png")
            
palette_dict = {(0, 0, 0, 0): b'\x00', (0, 0, 0, 255): b'\x01', (255, 0, 0, 255): b'\x02', (255, 115, 0, 255): b'\x03', (255, 255, 0, 255): b'\x04', (0, 255, 0, 255): b'\x05', (57, 115, 57, 255): b'\x06', (0, 255, 255, 255): b'\x07', (0, 0, 255, 255): b'\x08', (231, 115, 181, 255): b'\t', (255, 181, 115, 255): b'\n', (181, 115, 0, 255): b'\x0b', (115, 0, 0, 255): b'\x0c', (57, 57, 57, 255): b'\r', (156, 156, 156, 255): b'\x0e', (255, 255, 255, 255): b'\x0f', (255, 57, 0, 255): b'\x10', (231, 115, 0, 255): b'\x11', (57, 0, 0, 255): b'\x12', (0, 181, 0, 255): b'\x13', (57, 181, 0, 255): b'\x14', (115, 181, 0, 255): b'\x15', (181, 181, 0, 255): b'\x16', (231, 181, 0, 255): b'\x17', (255, 181, 0, 255): b'\x18', (0, 231, 0, 255): b'\x19', (57, 231, 0, 255): b'\x1a', (115, 231, 0, 255): b'\x1b', (181, 231, 0, 255): b'\x1c', (231, 231, 0, 255): b'\x1d', (255, 231, 0, 255): b'\x1e', (181, 0, 0, 255): b'\x1f', (57, 255, 0, 255): b' ', (115, 255, 0, 255): b'!', (181, 255, 0, 255): b'"', (231, 255, 0, 255): b'#', (57, 57, 0, 255): b'$', (0, 0, 57, 255): b'%', (57, 0, 57, 255): b'&', (115, 0, 57, 255): b"'", (181, 0, 57, 255): b'(', (231, 0, 57, 255): b')', (255, 0, 57, 255): b'*', (0, 57, 57, 255): b'+', (231, 0, 0, 255): b',', (115, 57, 57, 255): b'-', (181, 57, 57, 255): b'.', (231, 57, 57, 255): b'/', (255, 57, 57, 255): b'0', (0, 115, 57, 255): b'1', (0, 115, 0, 255): b'2', (115, 115, 57, 255): b'3', (181, 115, 57, 255): b'4', (231, 115, 57, 255): b'5', (255, 115, 57, 255): b'6', (0, 181, 57, 255): b'7', (57, 181, 57, 255): b'8', (115, 181, 57, 255): b'9', (181, 181, 57, 255): b':', (231, 181, 57, 255): b';', (255, 181, 57, 255): b'<', (0, 231, 57, 255): b'=', (57, 231, 57, 255): b'>', (115, 231, 57, 255): b'?', (181, 231, 57, 255): b'@', (231, 231, 57, 255): b'A', (255, 231, 57, 255): b'B', (0, 255, 57, 255): b'C', (57, 255, 57, 255): b'D', (115, 255, 57, 255): b'E', (181, 255, 57, 255): b'F', (231, 255, 57, 255): b'G', (255, 255, 57, 255): b'H', (0, 0, 115, 255): b'I', (57, 0, 115, 255): b'J', (115, 0, 115, 255): b'K', (181, 0, 115, 255): b'L', (231, 0, 115, 255): b'M', (255, 0, 115, 255): b'N', (0, 57, 115, 255): b'O', (57, 57, 115, 255): b'P', (115, 57, 115, 255): b'Q', (181, 57, 115, 255): b'R', (231, 57, 115, 255): b'S', (255, 57, 115, 255): b'T', (0, 115, 115, 255): b'U', (57, 115, 115, 255): b'V', (115, 115, 115, 255): b'W', (181, 115, 115, 255): b'X', (231, 115, 115, 255): b'Y', (255, 115, 115, 255): b'Z', (0, 181, 115, 255): b'[', (57, 181, 115, 255): b'\\', (115, 181, 115, 255): b']', (181, 181, 115, 255): b'^', (231, 181, 115, 255): b'_', (231, 57, 0, 255): b'`', (0, 231, 115, 255): b'a', (57, 231, 115, 255): b'b', (115, 231, 115, 255): b'c', (181, 231, 115, 255): b'd', (231, 231, 115, 255): b'e', (255, 231, 115, 255): b'f', (0, 255, 115, 255): b'g', (57, 255, 115, 255): b'h', (115, 255, 115, 255): b'i', (181, 255, 115, 255): b'j', (231, 255, 115, 255): b'k', (255, 255, 115, 255): b'l', (0, 0, 181, 255): b'm', (57, 0, 181, 255): b'n', (115, 0, 181, 255): b'o', (181, 0, 181, 255): b'p', (231, 0, 181, 255): b'q', (255, 0, 181, 255): b'r', (0, 57, 181, 255): b's', (57, 57, 181, 255): b't', (115, 57, 181, 255): b'u', (181, 57, 181, 255): b'v', (231, 57, 181, 255): b'w', (255, 57, 181, 255): b'x', (0, 115, 181, 255): b'y', (57, 115, 181, 255): b'z', (115, 115, 181, 255): b'{', (181, 115, 181, 255): b'|', (181, 57, 0, 255): b'}', (255, 115, 181, 255): b'~', (0, 181, 181, 255): b'\x7f', (57, 181, 181, 255): b'\x80', (115, 181, 181, 255): b'\x81', (181, 181, 181, 255): b'\x82', (231, 181, 181, 255): b'\x83', (255, 181, 181, 255): b'\x84', (0, 231, 181, 255): b'\x85', (57, 231, 181, 255): b'\x86', (115, 231, 181, 255): b'\x87', (181, 231, 181, 255): b'\x88', (231, 231, 181, 255): b'\x89', (255, 231, 181, 255): b'\x8a', (0, 255, 181, 255): b'\x8b', (57, 255, 181, 255): b'\x8c', (115, 255, 181, 255): b'\x8d', (181, 255, 181, 255): b'\x8e', (231, 255, 181, 255): b'\x8f', (255, 255, 181, 255): b'\x90', (0, 0, 231, 255): b'\x91', (57, 0, 231, 255): b'\x92', (115, 0, 231, 255): b'\x93', (181, 0, 231, 255): b'\x94', (231, 0, 231, 255): b'\x95', (255, 0, 231, 255): b'\x96', (0, 57, 231, 255): b'\x97', (57, 57, 231, 255): b'\x98', (115, 57, 231, 255): b'\x99', (181, 57, 231, 255): b'\x9a', (231, 57, 231, 255): b'\x9b', (255, 57, 231, 255): b'\x9c', (0, 115, 231, 255): b'\x9d', (57, 115, 231, 255): b'\x9e', (115, 115, 231, 255): b'\x9f', (181, 115, 231, 255): b'\xa0', (231, 115, 231, 255): b'\xa1', (255, 115, 231, 255): b'\xa2', (0, 181, 231, 255): b'\xa3', (57, 181, 231, 255): b'\xa4', (115, 181, 231, 255): b'\xa5', (181, 181, 231, 255): b'\xa6', (231, 181, 231, 255): b'\xa7', (255, 181, 231, 255): b'\xa8', (0, 231, 231, 255): b'\xa9', (57, 231, 231, 255): b'\xaa', (115, 231, 231, 255): b'\xab', (181, 231, 231, 255): b'\xac', (231, 231, 231, 255): b'\xad', (255, 231, 231, 255): b'\xae', (0, 255, 231, 255): b'\xaf', (57, 255, 231, 255): b'\xb0', (115, 255, 231, 255): b'\xb1', (181, 255, 231, 255): b'\xb2', (231, 255, 231, 255): b'\xb3', (255, 255, 231, 255): b'\xb4', (0, 57, 0, 255): b'\xb5', (57, 0, 255, 255): b'\xb6', (115, 0, 255, 255): b'\xb7', (181, 0, 255, 255): b'\xb8', (231, 0, 255, 255): b'\xb9', (255, 0, 255, 255): b'\xba', (0, 57, 255, 255): b'\xbb', (57, 57, 255, 255): b'\xbc', (115, 57, 255, 255): b'\xbd', (181, 57, 255, 255): b'\xbe', (231, 57, 255, 255): b'\xbf', (255, 57, 255, 255): b'\xc0', (0, 115, 255, 255): b'\xc1', (57, 115, 255, 255): b'\xc2', (115, 115, 255, 255): b'\xc3', (181, 115, 255, 255): b'\xc4', (231, 115, 255, 255): b'\xc5', (255, 115, 255, 255): b'\xc6', (0, 181, 255, 255): b'\xc7', (57, 181, 255, 255): b'\xc8', (115, 181, 255, 255): b'\xc9', (181, 181, 255, 255): b'\xca', (231, 181, 255, 255): b'\xcb', (255, 181, 255, 255): b'\xcc', (0, 231, 255, 255): b'\xcd', (57, 231, 255, 255): b'\xce', (115, 231, 255, 255): b'\xcf', (181, 231, 255, 255): b'\xd0', (231, 231, 255, 255): b'\xd1', (255, 231, 255, 255): b'\xd2', (115, 57, 0, 255): b'\xd3', (57, 255, 255, 255): b'\xd4', (115, 255, 255, 255): b'\xd5', (181, 255, 255, 255): b'\xd6', (231, 255, 255, 255): b'\xd7', (115, 115, 0, 255): b'\xd8', (24, 24, 24, 255): b'\xd9', (41, 41, 41, 255): b'\xda', (82, 82, 82, 255): b'\xdb', (99, 99, 99, 255): b'\xdc', (57, 115, 0, 255): b'\xdd', (132, 132, 132, 255): b'\xde', (206, 206, 206, 255): b'\xdf'}


inv_palette = {v: k for k, v in palette_dict.items()}

golden_sun = bytearray(open(game, "rb").read())


for character in battle_pointer_dict["TBS"].keys(): 
    pointerTable_start = battle_pointer_dict["TBS"][character]
    export_character(golden_sun, character, pointerTable_start, inv_palette)

