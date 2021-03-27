# sLOUT by Sidpatchy
# A small helper library used in several of my projects
# If you experience any issues, please open an issue on the GitHub: https://github.com/Sidpatchy/sLOUT

import yaml

# readConfig() configuration reader
# Usage:
#   file: string, file to read from
#   parameter: string, name of "varible" in config file, must be exact.
# Structure of config file:
# parameter = put stuff here
def readConfig(file, parameter):
    with open(file) as f:
        config = yaml.safe_load(f)
    return config[parameter]