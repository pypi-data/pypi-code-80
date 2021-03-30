"""Module that allow the authentification by register the personnal token"""

import getpass
import json
from pathlib import Path


def login_args_configuration(sub_parser):
    """
    Login subparser that add the default login function to the parser
    """
    login_parser = sub_parser.add_parser(name="login", help="login to deepchain")
    login_parser.set_defaults(func=login)


def login(_):
    """
    Login function that create a subdirectory and store the token
    """
    path = Path.home().joinpath(".deep-chain")
    path.mkdir(exist_ok=True)
    path = path.joinpath("config")

    data = {}
    with open(path, "w+") as config_file:
        try:
            data = json.load(config_file)
        finally:
            pass
        data["pat"] = getpass.getpass("PAT:")
        data["size_limit"] = 40
        json.dump(data, config_file)
