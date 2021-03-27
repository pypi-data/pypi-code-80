import yaml


class Emotes:
    # Useful emotes
    white_check_mark = '✅'

    # Todo - Add more emotes

    # Methods
    def __init__(self, category):
        self.category = category

    def get(self, item, default=None):
        return self.__getitem__(item) or default

    def __getitem__(self, item):
        import pkgutil

        data = pkgutil.get_data(__name__, f'{self.category}.yml')
        data = yaml.safe_load(data)

        return data.get(item, None)


People = Emotes('people')
Nature = Emotes('nature')
Food = Emotes('food')
Activities = Emotes('activities')
Travel = Emotes('travel')
Objects = Emotes('objects')
Symbols = Emotes('symbols')
Flags = Emotes('flags')
