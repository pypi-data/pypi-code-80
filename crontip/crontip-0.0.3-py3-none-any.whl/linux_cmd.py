"""Define the functions that used for
execute a command,
get output from it,
get the result from it(is error exist?)
"""


# Standard library imports
import subprocess


def run_cmd(cmd: str):
    """
    Executing a command.
    """
    return subprocess.run(cmd, shell=True)


def get_result(cmd: str):
    """
    Return the result of executing a command.
    """
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)


def get_output(cmd: str):
    """
    Return the result of executing a command.
    """
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return output.stdout[:-1]
