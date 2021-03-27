# sLOUT by Sidpatchy
# A small helper library used in several of my projects
# If you experience any issues, please open an issue on the GitHub: https://github.com/Sidpatchy/sLOUT

import yaml
from .writeFile import writeFile

# writeConfig() configuration writer
# WARNING: Strips all comments
# Usage:
#   file: string, file to read from
#   parameter: string, name of "varible" in config file, must be exact.
#   value: string, new value for "variable" in config file.
def writeConfig(file, parameter, value):
    writeFile(file, "{}:".format(parameter))
    with open(file) as f:
        config = yaml.safe_load(f)
    with open(file, 'w') as f:
        config[parameter] = value
        config = yaml.safe_dump(config, f)
    return True