# Modules
import os
import colorama
import subprocess

# Text holder
class AsciiHolder(object):

    """Takes ascii text and converts it using colorama"""

    def not_active(self, text):
        return text

    def is_active(self, text):
        return colorama.Back.LIGHTBLACK_EX + text + colorama.Back.RESET

# Clear function
def clear():

    command = "clear"
    if os.name == "nt":
        command = "cls"

    subprocess.run([command], shell = True)
