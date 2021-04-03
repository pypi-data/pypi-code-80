class bcolors:
    White = '\033[97m'
    Purple = '\033[95m'
    Blue = '\033[94m'
    Yellow = '\033[93m'
    Green = '\033[92m'
    Red = '\033[91m'
    Grey = '\033[90m'

    Normal = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# print(f'{bcolors.Green}User "{bcolors.BOLD}Arik{bcolors.Normal}{bcolors.Green}" Added!{bcolors.Normal}')

def printPurple(text):
    """
    Parameters
    ----------
    text : str
        the text value from user
    """
    print(f"{bcolors.Purple}{text}{bcolors.Normal}")

def printBlue(text):
    """
    Parameters
    ----------
    text : str
        the text value from user
    """
    print(f"{bcolors.Blue}{text}{bcolors.Normal}")

def printYellow(text):
    """
    Parameters
    ----------
    text : str
        the text value from user
    """
    print(f"{bcolors.Yellow}{text}{bcolors.Normal}")

def printGreen(text):
    """
    Parameters
    ----------
    text : str
        the text value from user
    """
    print(f"{bcolors.Green}{text}{bcolors.Normal}")

def printRed(text):
    """
    Parameters
    ----------
    text : str
        the text value from user
    """
    print(f"{bcolors.Red}{text}{bcolors.Normal}")

def printGrey(text):
    """
    Parameters
    ----------
    text : str
        the text value from user
    """
    print(f"{bcolors.Grey}{text}{bcolors.Normal}")

def printBold(text):
    """
    Parameters
    ----------
    text : str
        the text value from user
    """
    print(f"{bcolors.BOLD}{text}{bcolors.Normal}")

def printUnderline(text):
    """
    Parameters
    ----------
    text : str
        the text value from user
    """
    print(f"{bcolors.UNDERLINE}{text}{bcolors.Normal}")


# delete dist folder
# run py setup.py sdist