import pyHPump.util as util

gCountCmd = 0

"""
Zx - Initialize PSD/4, Assign Valve Output to Right
Yx - Initialize PSD/4, Assign Valve Output to Left
Wx - Initialize PSD/4, Configure for No Valve
"""


def initialize(drive: str, value=0):
    cmd: str = ''
    if drive == 'Z' or drive == 'Y' or drive == 'W':
        cmd += drive
    else:
        print("Error! Incorrect drive!")
        cmd = 'cmdError'
        return cmd
    if (value == 1) or (value >= 10 and value <= 40):
        cmd += str(value)
    else:
        print("Wrong parameter value for initialize command!")
        cmd = 'cmdError'
    return cmd


"""
R - Execute Command Buffer
X - Execute Command Buffer from Beginning
"""


def executeCommandBuffer(type='R'):
    cmd: str = ''
    if type == 'R' or type == 'X':
        cmd += type
    else:
        print("Error! Incorrect type!")
        cmd = 'cmdError'
    return cmd


"""
    Syringe Commands
"""


def setCounterPosition():
    return 'z'


def checkValueInInterval(value: int, valueST: int, valueHG: int):
    bVal: bool = False
    type: int = 0
    #get actual type -> TODO #standard sau high resolution mode
    #if standard mode
    if type == 0 and 0 <= value <= valueST:
        bVal = True
    elif type == 1 and 0 <= value <= valueHG:
        bVal = True
    else:
        print("Error - value out of range !!!")
    return bVal


def absolutePosition(value: int):
    #PSD4 - absolute position x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
    #PSD6 - absolute position x where 0 ≤ x ≤ 6,000 in standard mode or 0 ≤ x ≤ 48,000 in high resolution mode
    #PSD4sf - absolute position x where 0 ≤ x ≤ 192.000
    #PSD6sf - absolute position x where 0 ≤ x ≤ 384.000
    cmd: str = 'A'
    if checkValueInInterval(value, 3000, 24000):
        cmd += str(value)
    else:
        print("Wrong parameter value for absolute position command!")
        cmd = 'cmdError'
    return cmd


def absolutePositionWithReadyStatus(value: int):
    #absolute position x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
    cmd: str = 'a'
    if checkValueInInterval(value, 3000, 24000):
        cmd += str(value)
    else:
        print("Wrong parameter value for absolute position with ready status command!")
        cmd = 'cmdError'
    return cmd


def relativePickup(value: int):
    #PSD4 - absolute position x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
    #PSD6 - absolute position x where 0 ≤ x ≤ 6,000 in standard mode or 0 ≤ x ≤ 48,000 in high resolution mode
    #PSD4sf - absolute position x where 0 ≤ x ≤ 192.000
    #PSD6sf - absolute position x where 0 ≤ x ≤ 384.000
    cmd: str = 'P'
    if checkValueInInterval(value, 3000, 24000):
        cmd += str(value)
    else:
        print("Wrong parameter value for relative pickup command!")
        cmd = 'cmdError'
    return cmd


def relativePickupWithReadyStatus(value: int):
    #number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
    cmd: str = 'p'
    if checkValueInInterval(value, 3000, 24000):
        cmd += str(value)
    else:
        print("Wrong parameter value for relative pickup with ready status command!")
        cmd = 'cmdError'
    return cmd


def relativeDispense(value: int):
    #PSD4 - absolute position x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
    #PSD6 - absolute position x where 0 ≤ x ≤ 6,000 in standard mode or 0 ≤ x ≤ 48,000 in high resolution mode
    #PSD4sf - absolute position x where 0 ≤ x ≤ 192.000
    #PSD6sf - absolute position x where 0 ≤ x ≤ 384.000
    cmd: str = 'D'
    if checkValueInInterval(value, 3000, 24000):
        cmd += str(value)
    else:
        print("Wrong parameter value for relative dispense command!")
        cmd = 'cmdError'
    return cmd


def relativeDispenseWithReadyStatus(value: int):
    #number of steps x where 0 ≤ x ≤ 3,000 in standard mode or 0 ≤ x ≤ 24,000 in high resolution mode
    cmd: str = 'd'
    if checkValueInInterval(value, 3000, 24000):
        cmd += str(value)
    else:
        print("Wrong parameter value for relative dispense with ready status command!")
        cmd = 'cmdError'
    return cmd


def returnSteps(value: int):
    #Return Steps x where 0 ≤ x ≤ 100 in standard mode or 0 ≤ x ≤ 800 in high resolution mode
    #PSD6 - Return Steps x where 0 ≤ x ≤ 200 in standard mode or 0 ≤ x ≤ 1600 in high resolution mode
    #SmoothFlow - Return Steps x where 0 ≤ x ≤ 6400
    cmd: str = 'K'
    if checkValueInInterval(value, 100, 800):
        cmd += str(value)
    else:
        print("Wrong parameter value for return steps command!")
        cmd = 'cmdError'
    return cmd


def backoffSteps(value: int):
    #PSD4 - Back-off Steps x where 0 ≤ x ≤ 200 in standard mode and 0≤ x ≤ 1,600
    #PSD6 - Return Steps x where 0 ≤ x ≤ 100 in standard mode or 0 ≤ x ≤ 800 in high resolution mode
    #SmoothFlow - Return Steps x where 0 ≤ x ≤ 12.800
    cmd: str = 'k'
    if checkValueInInterval(value, 200, 1600):
        cmd += str(value)
    else:
        print("Wrong parameter value for backoff steps command!")
        cmd = 'cmdError'
    return cmd


"""
    Motor Commands
"""


def mStandardHighResolutionSelection(mode: int):
    #x=0 for standard resolution mode
    #x=1 for high resolution mode
    cmd: str = 'N'
    if mode == 0 or mode == 1:
        cmd += str(mode)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for standard/high resolution selection command!")
    return cmd


def mSetAcceleration(value: int):
    cmd: str = 'L'
    if 0 <= value <= 20:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for set acceleration command!")
    return cmd


def mSetStartVelocity(value: int):
    cmd: str = 'v'
    if 50 <= value <= 1000:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for set start velocity command!")
    return cmd


def mSetMaximumVelocity(value: int):
    cmd: str = 'V'
    if 2 <= value <= 5800:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for set maximum velocity command!")
    return cmd


def mSetSpeed(value: int):
    cmd: str = 'S'
    if 1 <= value <= 40:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for set speed command!")
    return cmd


def mStopVelocity(value: int):
    cmd: str = 'c'
    if 50 <= value <= 2700:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for stop velocity command!")
    return cmd


def mIncreaseStopVelocityBySteps(value: int):
    cmd: str = 'C'
    if 0 <= value <= 25:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Increase Stop Velocity by Steps command!")
    return cmd


"""
    Valve Commands
"""


def vMoveValveToInputPosition(value=0):
    cmd: str = 'I'
    if value == 0:
        print("Default command!")
    elif 1 <= value <= 8:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Move valve to input position command!")
    return cmd


def vMoveValveToOutputPosition(value=0):
    cmd: str = 'O'
    if value == 0:
        print("Default command!")
    elif 1 <= value <= 8:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Move valve to output position command!")
    return cmd


def vMoveValveToBypass():
    return 'B'


def vMoveValveToExtraPosition():
    return 'E'


"""
    Action commands
"""


def aDefinePositionInCommandString():
    cmd: str = 'g'
    global gCountCmd
    gCountCmd += 1
    if gCountCmd > 10:
        print("Using g command exceed maximum number of usage!")
        cmd = 'cmdError'
        gCountCmd = 0
    return cmd


#Gx - Repeat Commands
def aRepeatCommands(value=0):
    cmd: str = 'G'
    if value == 0:
        print("default value for Repeat Commands")
    elif 1 <= value <= 65535:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Repeat Commands command!")
    return cmd


#Mx - Delay - performs a delay of x milliseconds.where 5 ≤ x ≤ 30,000 milliseconds.
def aDelay(value: int):
    cmd: str = 'M'
    if 5 <= value <= 30000:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Delay command!")
    return cmd


#Hx - Halt Command Execution
def aHalt(value: int):
    cmd: str = 'H'
    if 0 <= value <= 2:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Halt command!")
    return cmd


#Jx - Auxiliary Outputs
def aAuxiliaryOutputs(value: int):
    cmd: str = 'J'
    if 0 <= value <= 7:
        cmd += str(value)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Auxiliary Outputs command!")
    return cmd


#sx - Store Command String
def aStoreCommandString(location: int, command: str):
    cmd: str = 's'
    if 0 <= location <= 14:
        cmd += str(location)
        cmd += command
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Store Command String command!")
    return cmd


#ex - Execute Command String in EEPROM Location
def aExecuteCommandStringInEEPROMLocation(location: int):
    cmd: str = 'e'
    if 0 <= location <= 14:
        cmd += str(location)
    else:
        cmd = 'cmdError'
        print("Wrong parameter value for Execute Command String in EEPROM Location command!")
    return cmd


"""
    Query Commands

queries = {
    'F': "Command Buffer Status",
    'Q': "Pump Status",
    '&': "Firmware Version",
    '#': "Firmware Checksum",
    '1': "Start Velocity",
    '2': "Maximum Velocity",
    '3': "Stop Velocity",
    '4': "Actual Position of Syringe",
    '12': "Number of Return Steps",
    '13': "Status of Auxiliary Input #1",
    '14': "Status of Auxiliary Input #2",
    '22': "Returns 255",
    '24': "Number of Back-off Steps",
    '10000': "Syringe Status",
    '10001': "Syringe Home Sensor Status",
    '11000': "Syringe Mode",
    '20000': "Valve Status",
    '21000': "Valve Type",
    '23000': "Valve Logical Position",
    '24000': "Valve Numerical Position",
    '25000': "Valve Angle",
    '37000': "Last Digital Out Value"
}
"""


def queryCommand(command: util.QueryCommandsEnumeration):
    return command.value


"""
h30001 - Enable h Factor Commands and Queries
h30000 - Disable h Factor Commands and Queries
"""


def hEnableFactorCommands(bValue: bool):
    cmd: str = 'h3000'
    cmd += str(int(bValue))
    return cmd


def hResetPSD():
    return "h30003"


def hInitializeValve():
    return "h20000"


def hInitializeSyringeOnly(speedCode: int):
    cmd: str = 'h'
    cmdValue = 10000
    #permitted values between 0-40
    if 0 <= speedCode <= 40:
        cmdValue += speedCode
    cmd += str(cmdValue)
    return cmd


def hSetSyringeMode(mode: int):
    cmd: str = 'h'
    cmdValue = 11000
    #permitted values between 0-15
    if 0 <= mode <= 15:
        cmdValue += mode
    cmd += str(cmdValue)
    return cmd


def hEnableValveMovement(bValue: bool):
    cmd: str = 'h2000'
    if bValue is True:
        cmd += '1'
    else:
        cmd += '2'
    return cmd


def hSetValveType(type: int):
    cmd: str = 'h2100'
    #permitted values between 0-6
    if 0 <= type <= 6:
        cmd += str(type)
    return cmd


def hMoveValveToSpecificPositionInShortestDirection(specificPosition: util.PositionInShortestDirection):
    cmd: str = 'h2300'
    cmd += str(specificPosition.value)
    return cmd


def hMoveValveClockwiseDirection(position: int):
    cmd: str = 'h2400'
    #permitted values between 1-8
    if 1 <= position <= 8:
        cmd += str(position)
    return cmd


def hMoveValveCounterclockwiseDirection(position: int):
    cmd: str = 'h2500'
    #permitted values between 1-8
    if 1 <= position <= 8:
        cmd += str(position)
    return cmd


def hMoveValveInShortestDirection(position: int):
    cmd: str = 'h2600'
    #permitted values between 1-8
    if 1 <= position <= 8:
        cmd += str(position)
    return cmd


def valveMovementHelper(cmdValue: int, incrementWith: int):
    cmd: str = 'h'
    #permitted values between 0-345 incremented by 15
    if 345 >= incrementWith >= 0 == incrementWith % 15:
        cmdValue += incrementWith
    cmd += str(cmdValue)
    return cmd


def hClockwiseAngularValveMove(position: int):
    return valveMovementHelper(27000, position)


def hCounterclockwiseAngularValveMove(position: int):
    return valveMovementHelper(28000, position)


def hShortestDirectAngularValveMove(position: int):
    return valveMovementHelper(29000, position)





