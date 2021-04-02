from .state import Potential


class Wave:
    def __init__(self, dims, states):
        self.dims = dims
        self.states = states
        self._grid = []

        for y in range(dims[0]):
            self._grid.append([])
            for x in range(dims[1]):
                self._grid[y].append(Potential(self.states))


    def pos(self, x, y) -> Potential:
        try:
            return self._grid[y][x]
        except IndexError:
            return Potential(self.states)


    def getstate(self, id):
        for state in self.states:
            if state.name == id:
                return state


    def gridmin(self):
        minimum = None
        for y, row in enumerate(self._grid):
            for x, item in enumerate(row):
                count = item.count(self, (x, y))
                if count is False:
                    continue

                if minimum is None or count < minimum[1]:
                    minimum = [(x, y), count]
        return minimum


    def collapse(self, presets: dict = {}):
        minimum = self.gridmin()

        while minimum:
            self.pos(*minimum[0]).collapse(self, minimum[0])
            minimum = self.gridmin()

        return self._grid[::-1]

