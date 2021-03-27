# sLOUT by Sidpatchy
# A small helper library used in several of my projects
# If you experience any issues, please open an issue on the GitHub: https://github.com/Sidpatchy/sLOUT

# Import libraries
from time import sleep
import datetime as DT

# writeFile() writes a string to the specified file
# Usage:
#   file: string, filename
#   string: string to be written to file.
#   time: Boolean, whether or not the time should be logged.
def writeFile(file, string, time=False):
    try:
        f = open(file, 'a')
        f.write(string)
        if time == True:
            f.write(' | {}'.format(str(DT.datetime.now())))
        f.write('\n')
        f.close()
    except:
        print('ERROR: Failed to write file. Make sure your user has permission to write to the file \'{}\'. If you have the correct permissions, please open an issue here: https://github.com/Sidpatchy/sLOUT'.format(file))
        writeFile('sLOUT-error.txt', 'ERROR: Failed to write file. Make sure your user has permission to write to the file \'{}\'. If you have the correct permissions, please open an issue here: https://github.com/Sidpatchy/sLOUT'.format(file), True)
        sleep(5)