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


def format_text(text):
    """
    Return a list of text.\n
    Remove the empty line in the end.
    """
    text = text.split('\n')

    if not text[-1]:
        text.pop()

    return text
