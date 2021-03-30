# Modules
import sys
import msvcrt

# Initialization
win_encoding = "mbcs"
XE0_OR_00 = "\x00\xe0"

# Main readchar function
def readchar(blocking = False):

    # Locate key
    while msvcrt.kbhit():
        msvcrt.getch()

    ch = msvcrt.getch()

    # Try and decode
    while ch.decode(win_encoding) in XE0_OR_00:
        msvcrt.getch()
        ch = msvcrt.getch()

    # Return our data
    return (
        ch
        if sys.version_info.major > 2
        else ch.decode(encoding=win_encoding)
    )
