TAKEN_CONSTANT_VALUES = []


class Constant:

    def __repr__(self):

        return self.get_repr()

    def __init__(self, value: int):

        if value not in TAKEN_CONSTANT_VALUES:

            self.__value = value

        else:

            raise ValueError(
                f'Cannot create constant with value \'{value}\' because a constant already exists with that value!')

    def get_value(self):

        return self.__value

    def get_repr(self):

        return f'<ServerCL:Constant of type ({self.get_value()})>'

    def compare(self, data_type):

        if self.get_repr() == data_type:
            return True
