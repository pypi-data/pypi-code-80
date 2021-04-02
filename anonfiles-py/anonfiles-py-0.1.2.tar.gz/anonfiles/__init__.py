from .anonfiles import AnonFiles, BayFiles

import sys

__version__ = "0.1.0"

# simple cli function
def cli():
    args = sys.argv

    # show help
    if len(args) <= 1:
        __show_help()
    if args[1] == "-h" or args[1] == "--help":
        __show_help()

    file = args[1]

    p = AnonFiles()
    print(p.upload(file))


def __show_help():
    print(
        """
 Anonfiles CLI Upload

   Usage: anonfiles [filename / path of file]
    """
    )
    quit(0)