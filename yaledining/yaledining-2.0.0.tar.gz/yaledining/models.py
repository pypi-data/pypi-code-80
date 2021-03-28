import datetime


class _base_model:
    def __init__(self, raw: dict, api):
        self.raw = raw
        for key in raw:
            setattr(self, key, raw[key])
        self.api = api


class Hall(_base_model):
    @property
    def managers(self):
        return self.api.hall_managers(self.id)

    def meals(self, *args, **kwargs):
        return self.api.meals(self.id, *args, **kwargs)


class Manager(_base_model):
    pass


class Meal(_base_model):
    @property
    def items(self):
        return self.api.items(self.id)


class Item(_base_model):
    @property
    def nutrition(self):
        return self.api.item_nutrition(self.id)


class Nutrition(_base_model):
    pass
