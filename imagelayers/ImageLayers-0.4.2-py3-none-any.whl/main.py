from PIL import Image, ImageDraw
from collections import defaultdict
import copy
import operator
from typing import Union

from .util import coordgen, nested_int_loop


def get_target_color(img):
    colorset = img.colorset()
    if img.image.format.upper() == 'JPEG':
        for i in range(256):
            if i not in colorset:
                return i
        return 0
    if img.image.format.upper() == 'PNG':
        for color in nested_int_loop([256] * len(img.load()[0,0])):
            if color not in colorset:
                return color
        return [0] * len(img.load()[0,0])

class ImageLayer:
    def __init__(self, image, pixelcoords, color):
        self.pxcs = set(pixelcoords)
        self.color = color if type(color) == int else tuple(color)
        self.image = image
    
    def add_pixel(self, x, y):
        self.pxcs = set(list(self.pxcs) + [(x,y)])

    def set_color(self, rgb):
        self.color = rgb
    
    def copy(self):
        return ImageLayer(self.image, copy.copy(self.pxcs), copy.copy(self.color))

    def __add__(self, other):
        pxcs = list(self.pxcs) + list(other.pxcs)
        return ImageLayer(self.image, pxcs, self.color)
    
    def __sub__(self, other):
        pxcs = [coord for coord in self.pxcs if coord not in other.pxcs]
        return ImageLayer(self.image, pxcs, color=self.color)

    def __pos__(self):
        return self.copy()
    
    def __neg__(self):
        pxcs = []
        for x in range(self.image.width):
            for y in range(self.image.height):
                if (x,y) not in self.pxcs:
                    pxcs.append((x,y))
        return ImageLayer(self.image, pxcs, copy.copy(self.color))
    
    def __eq__(self, other):
        return set(self.pxcs) == set(other.pxcs)

    def __or__(self, other):
        pxcs = [xy for xy in other.pxcs if xy in self.pxcs]
        return ImageLayer(self.image, pxcs, self.color)

    def __repr__(self):
        return f'<ImageLayer color={self.color}>'
    
    def save(self, *args, **kwargs):
        return self.toimage().save(*args, **kwargs)
    
    def toimage(self):
        img = Image.new(self.image.mode, self.image.size, self.color)
        px = img.load()
        for x, y in self.pxcs:
            px[x,y] = self.color
        return img
    
    def hexcolor(self, include_a=False):
        r,g,b,a = self.color
        color = (r,g,b,a) if include_a else (r,g,b)
        return '0x' + ''.join([hex(val)[2:].zfill(2) for val in color])

    def __len__(self):
        return len(self.pxcs)


class OptimalColors:
    def __init__(self, colors: tuple):
        for tup in colors:
            if type(tup) not in [list, tuple, int]:
                raise ValueError('Color must be tuple or list or int')
        self.colors = colors

    def adjustpixelrgb(self, pixel, limit=1, shift=0):
        print(pixel)
        r,g,b = pixel
        for mr,mg,mb in self.colors:
            if mr - limit + shift < r < mr + limit + shift and \
                mg - limit + shift < g < mg + limit + shift and \
                mb - limit + shift < b < mb + limit + shift:
                return mr,mg,mb
        return pixel
    
    def adjustpixelrgba(self, pixel, limit=1, shift=0):
        r,g,b,a = pixel
        for mr,mg,mb,ma in self.colors:
            if mr - limit + shift < r < mr + limit + shift and \
                mg - limit + shift < g < mg + limit + shift and \
                mb - limit + shift < b < mb + limit + shift and \
                ma - limit + shift < a < ma + limit +shift:
                return mr,mg,mb,ma
        return pixel
    
    def adjustpixelbw(self, pixel, limit=1, shift=0):
        for bw in self.colors:
            if bw - limit + shift < pixel < bw + limit + shift:
                return bw
        return pixel
    
    def optimize_image(self, image, tolerance=1, bwshift=0):
        px = image.load()
        for x,y in coordgen(*image.size):
                try:
                    px[x,y] = self.adjustpixelbw(px[x,y], tolerance, bwshift)
                except TypeError:
                    try:
                        px[x,y] = self.adjustpixelrgb(px[x,y], tolerance, bwshift)
                    except ValueError:
                        px[x,y] = self.adjustpixelrgba(px[x,y], tolerance, bwshift)
                

class ColorVector:
    def __init__(self, color: Union[int, tuple]):
        if type(color) == int:
            self.color = (color,)
        else:
            self.color = color
    
    def __add__(self, other):
        return self.op(other, operator.add)
    
    def __sub__(self, other):
        return self.op(other, operator.sub)
    
    def op(self, other, op):
        return ColorVector([op(a,b) for a,b in zip(self.color, other.color)])

    def function(self, func):
        return ColorVector([func(a) for a in zip(self.color)])

    def size(self):
        def distance(*args):
            if len(args) > 2:
                a, b, *c = args
                return distance((a**2+b**2)**0.5, *c)
            elif len(args) == 2:
                a, b = args
                return (a**2+b**2)**0.5
            elif len(args) == 1:
                return abs(args[0])
        return distance(*self.color)

class LayeredImage:
    def __init__(self, image):
        self.image = image
        
    def colorset(self):
        px = self.image.load()
        colors = [px[x,y] for x,y in coordgen(*self.image.size)]
        return set(colors)
    
    def layersbycolor(self):
        pixels = defaultdict(list)
        px = self.image.load()
        for x,y in coordgen(*self.image.size):
            pixels[str(px[x,y])].append((x,y))
        for color, coords in pixels.items():
            color = eval(color)
            yield ImageLayer(self.image, coords, color)

    def layersbyedge(self):
        orig = self.image.copy()
        target_color = get_target_color(self)
        px = orig.load()
        pixels = set()
        for x,y in coordgen(*orig.size):
                if (x,y) in pixels:
                    continue
                ImageDraw.floodfill(orig, xy=(x,y), value=target_color)
                group = filter(lambda x: px[x] == target_color, coordgen(*orig.size))
                layer = ImageLayer(self.image, group, color=target_color)
                del group
                for pixel in layer.pxcs:
                    if pixel not in pixels:
                        pixels.add(pixel)
                yield layer
                del layer

                orig = self.image.copy()
                px = orig.load()
        
    def optimize_color_boundaries(self, colors: tuple, *args, **kwargs):
        optcolors = OptimalColors(colors)
        optcolors.optimize_image(self.image, *args, **kwargs)

    def strictcolor(self, colors: tuple):
        px = self.image.load()
        def colordistance(a):
            return (ColorVector(px[x,y]) - ColorVector(a)).size()
        for x, y in coordgen(*self.image.size):
            choices = sorted(colors, key=lambda x: colordistance(x))
            px[x,y] = choices[0]