# Option handler
class OptionHandler(object):

    """The handler menus use for handling options"""

    def __init__(self):
        self.options = {}
        self.itercount = 1

    def __genid__(self):
        return len(self.options) + 1

    def __iter__(self):
        self.itercount = 1
        return self

    def __next__(self):

        try:
            self.itercount += 1
            return self.options[self.itercount - 1]

        except KeyError:
            raise StopIteration

    def add(self, text, callback):
        opt_id = self.__genid__()

        self.options[opt_id] = {
            "text": text,
            "callback": callback
        }

    def index(self, option):

        i = 0
        for opt in self.options:

            if self.options[opt] == option:
                return i

            i += 1

    def get(self, index):

        i = 0
        for opt in self.options:

            if i == index:
                return self.options[opt]

            i += 1
