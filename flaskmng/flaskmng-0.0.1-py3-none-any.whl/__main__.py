import sys
import click

from .manager import manager

commands = [
    manager
]


main = click.CommandCollection(sources=commands)

if __name__ == '__main__':
    args = sys.argv
    if "--help" in args or len(args) == 1:
        print("flaskmng")
    main()