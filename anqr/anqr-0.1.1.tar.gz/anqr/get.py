from PIL import Image
from errors import *

binaryString = ""

def parsePicture(file):
    global binaryString

    img = Image.open(file).convert('RGB')
    pixel = img.load()

    w=img.size[0]
    h=img.size[1]

    for i in range(w):
        for j in range(h):
            if pixel[i, j] == (255, 255, 255):
                binaryString += "1"
            elif pixel[i, j] == (0, 0, 0):
                binaryString += "0"
            elif pixel[i, j] == (160, 160, 160):
                binaryString += " "
            elif pixel[i, j] == (64, 64, 64) or pixel[i, j] == (128, 128, 128):
                break
            else:
                raise InvalidByteColorError(f"Invalid byte color at pixel {(w, h)}: {pixel[i, j]}")

def printOutcome():
    binary_values = binaryString.split()
    ascii_string = ""

    for binary_value in binary_values: ascii_string += chr(int(binary_value, 2))
    
    print(ascii_string)

def get(**kwargs) -> str:
    parsePicture(kwargs["file"])

    binaryValues = binaryString.split()
    asciiString = ""

    for binaryValue in binaryValues: asciiString += chr(int(binaryValue, 2))

    return asciiString