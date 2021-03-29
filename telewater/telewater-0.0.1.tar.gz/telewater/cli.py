# entry point to bot

from telewater.bot import run_single_bot
from telewater.settings import BOT_TOKEN

import sys


def main():
    args = sys.argv

    if len(args) == 3:
        name = args[1]
        token = args[2]
    elif len(args) == 1:
        if BOT_TOKEN:
            token = BOT_TOKEN
            name = token[:4]+token[-4:]

    run_single_bot(name, token)
