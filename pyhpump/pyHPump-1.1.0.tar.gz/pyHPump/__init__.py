from .psd import *
from .communication import init_serial
from .util import *
from .commands import *


#List of pumps. Initially the list is empty
pumps = []

def communicationInitialization(port, baudrate):
    communication.init_serial(port, baudrate)


def executeCommand(pump, command):
    communication.send_command(pump.asciiAddress, command)


def definePump(address: str, type=4, baudRate=9600, resolutionMode=0):
    pumps.append( PSD(address, type, baudRate, resolutionMode) )



