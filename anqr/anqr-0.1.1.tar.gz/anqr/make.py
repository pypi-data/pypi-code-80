from PIL import Image
from sys import stdout

def makePicture(string, filename):
    stdout.write('....')
    w, h = len(string), 8
    img = Image.new("L", (w, h), 0x7f)

    stdout.write('\r#...')
    pixels = []
    for value in (ord(ch) for ch in string):
        col = []
        mask = 0b10000000

        while mask:
            col.append(bool(value & mask) * 255)
            mask >>= 1
        
        pixels.append(col)
    
    stdout.write('\r##..')
    for x in range(w):
        for y in range(h):
            if y % 8 != 0:
                img.putpixel((x, y), pixels[x][y])
            else:
                img.putpixel((x, y), (160))
    stdout.write('\r###.')
    img.save(filename)
    stdout.write('\r####')