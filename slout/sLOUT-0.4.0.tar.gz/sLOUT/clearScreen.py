
# Import libraries
import platform
import os
from time import sleep

# Import other sLOUT modules
from .writeFile import writeFile

# clearScreen()
# Uses the appropriate clear command for your OS
def clearScreen():
    version = 'v0.3.0'
    OS = platform.system()
    if OS.upper() == 'LINUX' or OS.upper() == 'DARWIN':
        try:
            os.system('clear')          # Runs the command 'clear'
        except:
            print('ERROR: Unable to clear screen')
            print('       Please include the information below in a GitHub issue, along with your actual OS. https://github.com/Sidpatchy/sLOUT')
            print('       Detected OS: {}'.format(OS))
            writeFile('sLOUT-error.txt', 'ERROR: Unable to clear screen \n       Please include the information below in a GitHub issue, along with your actual OS. https://github.com/Sidpatchy/sLOUT \n       Detected OS: {} \n       sLOUT version: {}'.format(OS, version), True)
            sleep(5)

    elif OS.upper() == 'WINDOWS':
        try:
            os.system('cls')            # Runs the command 'cls'
        except:
            print('ERROR: Unable to clear screen')
            print('       Please include the information below in a GitHub issue, along with your actual OS. https://github.com/Sidpatchy/sLOUT')
            print('       Detected OS: {}'.format(OS))
            print('       sLOUT version: {}'.format(version))
            writeFile('sLOUT-error.txt', 'ERROR: Unable to clear screen \n       Please include the information below in a GitHub issue, along with your actual OS. https://github.com/Sidpatchy/sLOUT \n       Detected OS: {} \n       sLOUT version: {}'.format(OS, version), True)
            sleep(5)
    else:
        print('ERROR: The OS I detected ({}) is not supported. Please open a GitHub issue here: https://github.com/Sidpatchy/sLOUT')
        writeFile('sLOUT-error.txt', 'ERROR: The OS I detected ({}) is not supported. Please open a GitHub issue here: https://github.com/Sidpatchy/sLOUT')
        sleep(5)