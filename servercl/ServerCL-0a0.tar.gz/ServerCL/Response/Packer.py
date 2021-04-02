from ServerCL.Constant.Const import Constant
from ServerCL.Constant.Variables import *

class Packer:

    def __init__(self):

        self.__pack_methods = {}
        self.__unpack_methods = {}

    def console_alert(self, message):

        print('<< ATTENTION >> Packer.)', message)

    def get_pack_methods(self):

        return self.__pack_methods

    def get_unpack_methods(self):

        return self.__unpack_methods

    def get_pack_method(self, packed_type: Constant):

        return self.__pack_methods[packed_type] if packed_type in self.__pack_methods else None

    def get_unpack_method(self, packed_type: Constant):

        return self.__unpack_methods[packed_type] if packed_type in self.__unpack_methods else None

    def pack(self, data_type: Constant, data, pack_method=None):

        pack_method = self.default_packer if pack_method is None else pack_method

        return pack_method(data_type, data)

    def unpack(self, data: str):

        unpacked_data = None

        for data_type in self.get_unpack_methods():

            if unpacked_data := self.get_unpack_method(data_type)(data):

                break

        if not unpacked_data:

            self.console_alert(f'A NoneType object was forced to be passed through the \'Packer.unpack()\' method because there was no unpack method registered for {data}\'s data type.')

        return unpacked_data

    def register_pack_method(self, data_type: Constant):

        self.console_alert('Registered new packing method')

        def pack_method(method):

            self.__pack_methods[data_type] = method

            return method

        return pack_method

    def register_unpack_method(self, data_type: Constant):

        self.console_alert('Registered new unpacking method')

        def unpack_method(method):

            self.__unpack_methods[data_type] = method

            return method

        return unpack_method

    def default_interpreter(self, information: str) -> (Constant, str):

        self.console_alert('Interpreted message')

        data_type = ''
        char = 0

        while information[char] != '>':
            data_type += information[char]
            char += 1

        data_type += information[char]
        char += 1

        return data_type, information[char:]

    def default_packer(self, data_type: Constant, data):

        return f'{data_type}{data}'


PACKER = Packer()

""" String Unpacker """

@PACKER.register_unpack_method(STRING)
def unpack_string(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if STRING.compare(data_type):

        try:

            unpacked_info = str(unpacked_information)

            return unpacked_info

        except:

            pass


""" Number Unpackers """


@PACKER.register_unpack_method(INTEGER)
def unpack_integer(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if INTEGER.compare(data_type):

        try:

            unpacked_info = int(unpacked_information)

            return unpacked_info

        except:

            pass

@PACKER.register_unpack_method(FLOAT)
def unpack_float(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if FLOAT.compare(data_type):

        try:

            unpacked_info = float(unpacked_information)

            return unpacked_info

        except:

            pass


@PACKER.register_unpack_method(COMPLEX)
def unpack_complex(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if COMPLEX.compare(data_type):

        try:

            unpacked_info = complex(unpacked_information)

            return unpacked_info

        except:

            pass


""" List Unpackers """


@PACKER.register_unpack_method(LIST)
def unpack_list(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if LIST.compare(data_type):

        try:

            unpacked_info = list(unpacked_information)

            return unpacked_info

        except:

            pass


@PACKER.register_unpack_method(TUPLE)
def unpack_tuple(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if TUPLE.compare(data_type):

        try:

            unpacked_info = tuple(unpacked_information)

            return unpacked_info

        except:

            pass


@PACKER.register_unpack_method(RANGE)
def unpack_range(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if RANGE.compare(data_type):

        try:

            unpacked_info = range(unpacked_information)

            return unpacked_info

        except:

            pass


""" Dict Unpacker """


@PACKER.register_unpack_method(DICT)
def unpack_dict(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if DICT.compare(data_type):

        try:

            unpacked_info = dict(unpacked_information)

            return unpacked_info

        except:

            pass


""" Set Unpackers """


@PACKER.register_unpack_method(SET)
def unpack_set(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if SET.compare(data_type):

        try:

            unpacked_info = set(unpacked_information)

            return unpacked_info

        except:

            pass


@PACKER.register_unpack_method(FROZENSET)
def unpack_frozenset(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if FROZENSET.compare(data_type):

        try:

            unpacked_info = frozenset(unpacked_information)

            return unpacked_info

        except:

            pass


""" Boolean Unpacker """


@PACKER.register_unpack_method(BOOLEAN)
def unpack_boolean(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if BOOLEAN.compare(data_type):

        try:

            unpacked_info = bool(unpacked_information)

            return unpacked_info

        except:

            pass


""" Byte Unpackers """


@PACKER.register_unpack_method(BYTES)
def unpack_bytes(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if BYTES.compare(data_type):

        try:

            unpacked_info = bytes(unpacked_information)

            return unpacked_info

        except:

            pass


@PACKER.register_unpack_method(BYTEARRAY)
def unpack_bytearray(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if BYTEARRAY.compare(data_type):

        try:

            unpacked_info = bytearray(unpacked_information)

            return unpacked_info

        except:

            pass


@PACKER.register_unpack_method(MEMORYVIEW)
def unpack_memoryview(data):
    data_type, unpacked_information = PACKER.default_interpreter(data)

    if MEMORYVIEW.compare(data_type):

        try:

            unpacked_info = memoryview(unpacked_information)

            return unpacked_info

        except:

            pass

    else:

        return None
