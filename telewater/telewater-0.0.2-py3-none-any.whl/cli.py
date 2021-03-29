# entry point to bot

from telewater.bot import run_single_bot
from telewater.settings import BOT_TOKEN

import sys


def main():
    args = sys.argv
    name, token = None, None
    if len(args) == 3:
        name = args[1]
        token = args[2]
    elif len(args) == 1:
        if BOT_TOKEN:
            token = BOT_TOKEN
            name = token[:4]+token[-4:]
        else:
            return

    run_single_bot(name, token)


