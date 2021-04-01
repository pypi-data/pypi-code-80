from .framework._application import (
    _app as app,
    )

version = '01.00.006'

def root_init(name: str, file) -> bool:
    import os

    if name != "__main__":
        return False

    elif os.path.abspath(file) == os.getcwd():
        pass

    else:
        test = file[:file.rfind("\\") + 1]
        os.chdir(test)

    from .packaet import system_message
    system_message("launching the project directly...")

    return True

__version__ = version

__title__ = 'TestCanaryBot ' + version
__author__ = 'Kensoi'
__license__ = 'Apache v2'
__copyright__ = 'Copyright 2021 kensoi'

__doc__ = "kensoi/testcanarybot, " + version + """
Documentation is available at kensoi.github.io/testcanarybot
"""

__all__ = ['version', 'app', 'root_init']