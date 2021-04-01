import pyHPump.util as util


class PSD:
    # default address in case that psd has address pin set on 0
    asciiAddress = "1"
    # default value id DIP switch bit 3 is OFF
    baudRate = 9600
    # standard resolution has value 0 = 3000 steps
    resolutionMode = 0
    # type of PSD: 4 / 6 / 4sf / 6sf, most used is psd4
    type = util.PSDTypes.psd4

    def __init__(self, address: str, type: util.PSDTypes, baudRate=9600, resolutionMode=0):
        self.setAddress(address)
        self.type = type
        self.baudRate = baudRate
        self.resolutionMode = resolutionMode


    def setAddress(self, address):
        translateAddress = {
            '0': "1",
            '1': "2",
            '2': "3",
            '3': "4",
            '4': "5",
            '5': "6",
            '6': "7",
            '7': "8",
            '8': "9",
            '9': ":",
            'A': ";",
            'B': "<",
            'C': "=",
            'D': ">",
            'E': "?",
            'F': "@",
        }
        self.asciiAddress = translateAddress.get(address, "1")

    def setValve(self):
        #give permision for query commands
        pass
        #read DIP switch bits 4-6

    def print(self):
        print("Address: " + self.asciiAddress)
        print("Type: " + str(self.type))
        print("BaudRate: " + str(self.baudRate))
        print("ResolutionMode: " + str(self.resolutionMode))



