from random import randint, choice
from PIL import Image

class Colour:

    def colour(self):
        r = randint(30, 225)
        g = randint(30, 225)
        b = randint(30, 225)
        return (r, g, b)

    def scheme(self, colour=None, bounds=20):

        if not colour:
            colour = self.colour()

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

    def schemes(self, amount=3, bounds=20):

        schemes = []
        for i in range(amount):
            while True:
                scheme = self.scheme(bounds=bounds)
                if scheme not in schemes:
                    schemes.append(scheme)
                    break

        return schemes

    def next(self, colour, colours):
        i = colours.index(colour)
        if i < 2: i += 1
        return colours[i]

    def heavy(self, colour1, colour2, colours):
        if colours.index(colour1) > colours.index(colour2):
            return colour1
        return colour2

def paint(coords, colours):

    center_x, center_y = coords
    outer = (THICKNESS - THICKNESS // 5)**2
    middle = (THICKNESS - round(THICKNESS / 5) * 2)**2
    radius = THICKNESS**2
    for x in range(center_x - THICKNESS, center_x + THICKNESS, 4):
        for y in range(center_y - THICKNESS, center_y + THICKNESS, 4):
            if x < 0 or y < 0 or y >= WIDTH or x >= WIDTH: continue
            
            X, Y = (x - center_x)**2, (y - center_y)**2
            if X + Y > radius: continue
            
            if X + Y > outer:
                #print(X, Y, outer)
                colour = colours[0]
            elif X + Y > middle:
                colour = colours[1]
            else:
                colour = colours[2]

            old_colour = pixels[x, y]
            if old_colour in colours:
                pixels[x, y] = Colours.heavy(colour, old_colour, colours)
            else:
                pixels[x, y] = colour
        

def mutate(coords, direction):

    def change(direction):
        if direction in BOUNDS[0:-1]:
            direction += choice([-1, 1])
        elif direction == BOUNDS[0]:
            direction += 1
        elif direction == BOUNDS[-1]:
            direction -= 1
        else:
            direction = choice([-1, 1])
        return direction
            
    mutation = randint(0, 100) + 1
    new_direction = list(direction)
    if mutation > STRAIGHTNESS:
        axis = randint(0, 1)
        new_direction[axis] = change(direction[axis])
    direction = tuple(new_direction)

    coords = (coords[0] + direction[0],
              coords[1] + direction[1])

    return (*coords, direction)

WIDTH = 1000
LINE_BOUNDS = (400, 500)
LINELEN_BOUNDS = (100, 500)
SMOOTHNESS = 10
THICKNESS = 20
STRAIGHTNESS = 50

BOUNDS = list(range(-SMOOTHNESS, SMOOTHNESS))
BOUNDS.pop(BOUNDS.index(0))

img = Image.new("RGB", (WIDTH, WIDTH), color=(255,255,255))
pixels = img.load()

Colours = Colour()
schemes = Colours.schemes(bounds=10)
for i in range(randint(*LINE_BOUNDS)):
    colours = choice(schemes)
    x, y = randint(0, WIDTH), randint(0, WIDTH)
    direction = (choice(BOUNDS), choice(BOUNDS))
    for i in range(randint(*LINELEN_BOUNDS)):
        paint((x, y), colours)
        x, y, direction = mutate((x, y), direction)
        
img.save("pixeltest.png")
