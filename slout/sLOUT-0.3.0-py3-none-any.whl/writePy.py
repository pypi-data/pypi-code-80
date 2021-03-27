# sLOUT by Sidpatchy
# A small helper library used in several of my projects
# If you experience any issues, please open an issue on the GitHub: https://github.com/Sidpatchy/sLOUT

# Import libraries
from time import sleep

# Import other sLOUT modules
from .writeFile import writeFile

# WILL BE REMOVED IN sLOUT v0.5.0
# writePy() essentially writeFile but targets a python fle in the directory bots/
# Usage:
#   file: string, filename
#   string: string to be written to file.
#   time: Boolean, whether or not the time should be logged.
def writePy(file, string, time=False):
    try:
        f = open('bots/{}.py'.format(file), 'a')
        f.write(string)
        if time == True:
            f.write(str(DT.datetime.now()))
        f.write('\n')
        f.close()
    except:
        print('ERROR: Failed to read file. Make sure your user has permission to write to the file \'bots/{}.py\'. If you have the correct permissions, please open an issue here: https://github.com/Sidpatchy/sLOUT'.format(file))
        writeFile('sLOUT-error.txt', 'ERROR: Failed to read file. Make sure your user has permission to write to the file \'bots/{}.py\'. If you have the correct permissions, please open an issue here: https://github.com/Sidpatchy/sLOUT'.format(file), True)
        sleep(5)