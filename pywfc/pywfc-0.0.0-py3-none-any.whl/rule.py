import typing as t


class Rule:
    def __init__(self, lmbda: t.Callable):
        self.lmbda = lmbda

    def check(self, wave, xy: tuple, constrain: bool = False):
        constraints = dict(self.lmbda(*xy))
        for xy2, states in constraints.items():
            for state in states:
                if state not in [x.name for x in wave.pos(*xy2).states]:
                    return False, constraints

        if constrain:
            for xy, states in constraints.items():
                wave.pos(*xy).constrain(
                    [wave.getstate(s) for s in states]
                )

        return True, constraints

    @staticmethod
    def constrain(coords: tuple, *states):
        return [coords, list(states)]

