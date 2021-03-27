# sLOUT by Sidpatchy
# A small helper library used in several of my projects
# If you experience any issues, please open an issue on the GitHub: https://github.com/Sidpatchy/sLOUT

# Import other sLOUT modules
from .readConfig import readConfig

# WILL BE REMOVED IN sLOUT v0.5.0
# fetchToken() reads the bot token from token.txt
# Usage:
#   configFile: string, name of configuration file
def fetchToken(configFile):
    return readConfig(configFile, 'token')