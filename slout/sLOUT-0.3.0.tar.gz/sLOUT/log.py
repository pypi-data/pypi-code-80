# sLOUT by Sidpatchy
# A small helper library used in several of my projects
# If you experience any issues, please open an issue on the GitHub: https://github.com/Sidpatchy/sLOUT

# Import libraries
from time import sleep
import datetime as DT

# Import other sLOUT modules
from .writeFile import writeFile
from .readConfig import readConfig

# log()
# Usage:
#   startTime: the time the command was initiated at, use a variable formed using datetime. import datetime and then use datetime.datetime.now()
#   processName: string, the name of the command/process that was run
#   botName: string, the name of the bot. Can be suplemented by placing the name you would like to use in a file named bot.txt
#   startup: boolean, when true, it will print done loading and the time. If you are using bot.txt insert lout.readFile('bot.txt') as the third parameter or just insert the bot name as a string.
def log(file, startTime=DT.datetime.now(), processName='Unknown', name=True, startup=False):
    if startup == True:

        # read the botname from the config
        botName = readConfig(file, 'botName')
        
        # Console Stuff
        print('--------------{}---------------'.format(botName))                # Divder in the console
        print('Time since startup: {}'.format(DT.datetime.now() - startTime))   # Prints how long it has been since the bot was started
        print('Current Time: {}'.format(DT.datetime.now()))                     # Prints the current time
        print('Done Loading!')                                                  # States that the bot is done loading
        print()                                                                 # SPACER!

        try:
            # Log stuff. This could all be achieved with one line but this looks better, it's slower but doesn't matter for now.
            writeFile('{}Logs.txt'.format(botName), '\n--------------{}---------------'.format(botName))
            writeFile('{}Logs.txt'.format(botName), 'Time since startup: {}'.format(DT.datetime.now() - startTime))
            writeFile('{}Logs.txt'.format(botName), 'Current Time: {}'.format(DT.datetime.now()))
            writeFile('{}Logs.txt'.format(botName), 'Done Loading!\n')
        except:
            print('ERROR: Unable to write to log file \'{}Logs.txt\'.'.format(botName))
            sleep(5)

    elif startup == False:
        # read the botname from the config
        botName = readConfig(file, 'botName')

        # Console Stuff
        print('--------------{}---------------'.format(botName))                # Divder in the console
        print('Current Time: {}'.format(DT.datetime.now()))                     # Prints the current time
        print('Time to run: {}'.format((DT.datetime.now() - startTime)))        # Subtracts the time passed in via startTime from the current time
        print('{} was run'.format(processName))                                 # States which process was run
        print()                                                                 # SPACER!

        try:
            # Log stuff. This could all be achieved with one line but this looks better, it's slower but doesn't matter for now.
            writeFile('{}Logs.txt'.format(botName), '\n--------------{}---------------'.format(botName))
            writeFile('{}Logs.txt'.format(botName), 'Current Time: {}'.format(DT.datetime.now()))
            writeFile('{}Logs.txt'.format(botName), 'Time to run: {}'.format((DT.datetime.now() - startTime)))
            writeFile('{}Logs.txt'.format(botName), '{} was run\n'.format(processName))
        except:
            print('ERROR: Unable to write to log file \'{}Logs.txt\'.'.format(botName))
            sleep(5)