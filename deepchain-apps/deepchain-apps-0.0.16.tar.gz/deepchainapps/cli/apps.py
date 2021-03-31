"""Commands to provide additional feature on app, such as list all the apps"""
import json
import os
import shutil
from json import JSONDecodeError
from pathlib import Path
from typing import Dict


def apps_args_configuration(sub_parser):
    """
    Main parser for apps info
    Define 'Deploy' as default function
    """
    login_parser = sub_parser.add_parser(
        name="apps", help="give infos on apps create locally"
    )

    login_parser.add_argument(
        "--infos",
        action="store_const",
        default=False,
        const=True,
        help="list all apps' infos",
    )

    login_parser.add_argument(
        "--reset",
        action="store_const",
        default=False,
        const=True,
        help="!reset all apps",
    )

    login_parser.set_defaults(func=apps_actions)


def get_apps_config() -> Dict:
    """
    Get app config files
    """
    path = Path.home().joinpath(".deep-chain").joinpath("apps")
    data = {}

    with open(path, "r") as apps_file:
        try:
            data = json.load(apps_file)
        except (FileNotFoundError, JSONDecodeError):
            pass

    return data


def display_config_infos(config: Dict) -> list:
    """Display apps infos """
    data_list = []
    data_list.append(["APP", "PATH", "STATUS"])
    for app, info in config.items():
        data_list.append([app, info["dir"], info["status"]])

    dash = "-" * 125

    for i, data in enumerate(data_list):
        if i == 0:
            print(dash)
            print("{:<20s}{:^90s}{:>15s}".format(data[0], data[1], data[2]))
            print(dash)
        else:
            print("{:<20s}{:^90s}{:>15s}".format(data[0], data[1], data[2]))

    return


def reset_apps() -> Dict:
    """
    Remove all apps' file
    """
    path = Path.home().joinpath(".deep-chain").joinpath("apps")
    apps_config = get_apps_config()

    if len(apps_config) > 0:
        for _, info in apps_config.items():
            try:
                shutil.rmtree(info["dir"])
            except FileNotFoundError:
                pass
        os.remove(str(path))
        path.touch(exist_ok=True)


def apps_actions(args):
    """main function for list apps infos"""
    if args.infos:
        config = get_apps_config()

        if len(config) == 0:
            print("-------------------")
            print("No apps to display")
            print("-------------------")
        else:
            display_config_infos(config)

    if args.reset:
        msg = "You are about to delete all your apps, do you want to continue? (y/n)"
        answer = input(msg)
        while answer not in ["y", "n"]:
            answer = input(msg)

        if answer == "y":
            reset_apps()
