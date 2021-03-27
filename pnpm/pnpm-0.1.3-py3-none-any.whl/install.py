from pathlib import Path
import site
from rich import print
import os
import subprocess as sp

def install():

    print("Installing pnpm...")

    # sp.call("pip install pnpm", shell=True)

    print('install location: ')
    print(site.getsitepackages())

    # if 'zsh' in os.environ.get("SHELL", ""):
    # print('Installing with zsh')
    # with open(Path.home() / ".zshrc", 'a') as f:
        # path = 'test'
        # f.write(f'alias pnpm="python3 cli.py"')
        

        