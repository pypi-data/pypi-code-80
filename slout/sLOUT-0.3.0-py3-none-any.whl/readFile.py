# sLOUT by Sidpatchy
# A small helper library used in several of my projects
# If you experience any issues, please open an issue on the GitHub: https://github.com/Sidpatchy/sLOUT

# Import libraries
from time import sleep

# Import other sLOUT modules
from .writeFile import writeFile

# readFile() reads a file
# Usage:
#   file: string, filename
def readFile(file):
    try:
        f = open(file, 'r')
        contents = f.read()
        f.close()
        return contents
    except:
        print('ERROR: Failed to read file. Make sure your user has permission to read the file \'{}\'. If you have the correct permissions, please open an issue here: https://github.com/Sidpatchy/sLOUT'.format(file))
        writeFile('sLOUT-error.txt', 'ERROR: Failed to read file. Make sure your user has permission to read the file \'{}\'. If you have the correct permissions, please open an issue here: https://github.com/Sidpatchy/sLOUT'.format(file), True)
        sleep(5)