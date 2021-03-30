# Modules
import sys
import tty
import termios

# Linux readchar
def readchar():

    # Get key from stdin
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # Return character
    return ch
