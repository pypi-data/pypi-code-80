from random import randint, choice
from PIL import Image        

class DirectionalMutation:

    def __init__(self, smoothness=1, mutation_chance=50):
        self.bounds = list(range(-smoothness, smoothness))
        self.bounds.pop(self.bounds.index(0))
        self.mutation_chance = self.mutation_chance

    def SemiRandomCurve(direction):

        def mutate(direction):
            if direction in self.bounds[0:-1]:
                direction += choice([-1, 1])
            elif direction == self.bounds[0]:
                direction += 1
            elif direction == self.bounds[-1]:
                direction -= 1
            else:
                direction = choice([-1, 1])
            return direction
                
        mutation = randint(0, 100) + 1
        direction = list(direction)
        if mutation > self.mutation_chance:
            axis = randint(0, 1)
            direction[axis] = mutate(direction[axis])

        return tuple(direction)
