# 1.0

import configparser

cfg = configparser.ConfigParser()
Link = "https://github.com/ivan-software/Ini-Reader/"

class INIReader:
    def IniRead(FILE):
        global cfg
        file = FILE
        cfg.read(file)
    def Read(BLOCK, VARIABLE, PRINT=1):
        global cfg
        block = BLOCK
        var = VARIABLE
        read = cfg[block][var]
        if PRINT == 1:
            print(read)
        if PRINT == 0:
            read = cfg[block][var]
    def Help():
        print(
        "IniRead - Read INI \n "
      	"Read - Read And Print INI \n "
      	"If PRINT = 0 - Data Will Not Print \n "
      	"If PRINT = 1 - Data Prints \n "
        "More on " + Link
        )


#-----/*\----------/*\----------/*\-----
__package__ = "INI-Reader"
__version__ = "1.0"
__author__ = "Ivan Perzhinskiy"
__mask__ = "ini_reader"
#-----/*\----------/*\----------/*\-----
