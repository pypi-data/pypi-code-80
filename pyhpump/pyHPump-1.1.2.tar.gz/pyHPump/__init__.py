from .psd import *
from .communication import init_serial
from .util import *
from .commands import *


#List of pumps. Initially the list is empty
pumps = []
pumpLenght = 16

def communicationInitialization(port, baudrate):
    communication.init_serial(port, baudrate)


def executeCommand(pump, command, waitForPump=False):
    result = commands.forwardType(pump.type)
    if result:
        communication.send_command(pump.asciiAddress, command, waitForPump)


def definePump(address: str, type=4, baudRate=9600, resolutionMode=0):
    if len(pumps) < pumpLenght:
        pumps.append( PSD(address, type, baudRate, resolutionMode) )





