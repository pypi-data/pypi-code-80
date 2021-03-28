from random import randint, choice

def Colour():
    r = randint(30, 225)
    g = randint(30, 225)
    b = randint(30, 225)
    return (r, g, b)
Color = Colour

def toHex(colour, prefix=False):
    hex_triplet = []
    for decimal in colour:
        hex_triplet.append(hex(decimal)[2:].upper())
    if not prefix:
        return "".join(hex_triplet)
    return "0x" + "".join(hex_triplet)

def toDecimal(colour, string=False):
    decimal = int(toHex(colour), 16)
    if not string:
        return decimal
    return str(decimal)

def toBinary(colour, prefix=False):
    binary = bin(toDecimal(colour))[2:]
    while len(binary) != 24:
        binary = "0" + binary
    binary_triplet = [binary[:8], binary[8:16], binary[16:]]
    if not prefix:
        return tuple(binary_triplet)
    for i in range(3):
        binary_triplet[i] = "0b" + binary_triplet[i]
    return tuple(binary_triplet)

def toPercent(colour):
    percentages = []
    for decimal in colour:
        percentage = round(decimal / 2.55, 1)
        percentages.append(percentage)
    percentages = tuple(percentages)
    return percentages

"""colour = Colour()
print(colour)
print(toHex(colour, prefix=True))
print(toDecimal(colour))
print(toBinary(colour, prefix=True))
print(toPercent(colour))"""

class Monochromatic:

    def ColourScheme(colour=None, color=None, bounds=20):

        if not colour or color:
            colour = Colour()
        elif color:
            colour = color

        upper_bound = []
        lower_bound = []

        for value in colour:
            upper = value + bounds
            lower = value - bounds
            while upper > 255:
                upper -= 1
            while lower < 0:
                lower += 1
            upper_bound.append(upper)
            lower_bound.append(lower)

        upper_bound = tuple(upper_bound)
        lower_bound = tuple(lower_bound)

        return (upper_bound, colour, lower_bound)

    class ColourSchemes:

        def __init__(self, amount=3, bounds=20):
            self.generate(amount=3, bounds=20)

        def generate(self, amount=3, bounds=20):
            self.schemes = []
            for i in range(amount):
                while True:
                    scheme = Monochromatic.ColourScheme(bounds=bounds)
                    if scheme not in schemes:
                        self.schemes.append(scheme)
                        break
            return self.schemes

        def random(self):
            return choice(self.schemes)

    ColorScheme = ColourScheme
    ColorSchemes = ColourSchemes
