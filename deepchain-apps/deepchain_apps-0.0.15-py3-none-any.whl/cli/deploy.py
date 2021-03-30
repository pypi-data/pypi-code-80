"""deploy modules helps for the deployement of application on deepchain"""

import argparse
import configparser
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List

import pkg_resources
import requests
from deepchainapps import AppNotFoundError, ConfigNotFoundError, log
from deepchainapps.utils.common import get_app_dir, get_scorer_configuration
from deepchainapps.utils.validation import _check_scorer_files


def deploy_args_configuration(sub_parser):
    """
    Main parser for deployement
    Define 'Deploy' as default function
    """
    login_parser = sub_parser.add_parser(
        name="deploy", help="deploy your app to deepchain"
    )
    login_parser.add_argument("app_name", action="store", help="app name")
    login_parser.add_argument(
        "--checkpoint",
        action="store",
        default=False,
        help="include checkpoint upload",
    )
    login_parser.set_defaults(func=deploy)


def deploy(args):
    """
    Deploy function:
        - Read config.ini
    upload checkpoints to deepchain
    """
    config = configparser.ConfigParser()
    path_config = pkg_resources.resource_filename("deepchainapps", "cli/config.ini")
    config.read(path_config)
    url = config["APP"]["DEEP_CHAIN_URL"]

    configuration = get_configuration()
    pat = configuration["pat"]

    app_name = args.app_name
    app_dir = get_app_dir(app_name)
    log.info("Check files before upload...")
    _check_scorer_files(app_name)
    # score_configuration = get_scorer_configuration(app_name)
    score_configuration = ["test"]

    req = upload_code(app_dir, args, pat, url, score_configuration)

    if req.status_code != 200:
        log.warning(f"api return {req.status_code} stopping operation")
        return

    log.info("App has been uploaded.")
    if args.checkpoint:
        # upload_checkpoint(args,app_name, pat, url, configuration["size_limit"])
        pass

    return


def upload_code(
    app_dir: str,
    args: argparse.ArgumentParser,
    pat: str,
    url: str,
    score_configuration: List[str],
):
    """
    Function to compress and upload code to google cloud bucket
    """
    archive = shutil.make_archive(args.app_name, "zip", root_dir=app_dir + "/src")
    with open("scores.json", "w+") as config_file:
        json.dump(score_configuration, config_file)

    req = requests.post(
        url=url + args.app_name,
        headers={"authorisation": pat},
        files={
            "code": ("code.zip", open(archive, "rb"), "application/octet-stream"),
            "configuration": (
                "scores.json",
                open("scores.json", "rb"),
                "application/json",
            ),
        },
    )

    os.remove(archive)
    os.remove("scores.json")
    return req


def get_configuration() -> str:
    """
    Get personal access token. User must use 'login' function at least once
    Get maximal file size can be uploaded. User must use 'login' function at least once
    """
    path = Path.home().joinpath(".deep-chain").joinpath("config")
    with open(path, "r") as config_file:
        try:
            data = json.load(config_file)
        except FileNotFoundError as err:
            raise ConfigNotFoundError from err
    return data


def upload_checkpoint(
    args: argparse.ArgumentParser, app_name: str, pat: str, url: str, size_limit: int
):
    """
    Zip checkpoints files and upload to deepchain
    """
    signed_url = get_object_storage_url(args, pat, url)
    app_name = args.app_name
    app_dir = get_app_dir(app_name)

    archive = shutil.make_archive(
        "checkpoint",
        "zip",
        app_dir + "/checkpoint",
    )
    if os.stat(archive).st_size / (1024 * 1024) > size_limit:
        print(f"Can not upload files over {size_limit}MB")
    else:
        requests.put(
            signed_url, files={"checkpoints": ("checkpoints.zip", open(archive, "rb"))}
        )
    os.remove(archive)


def get_object_storage_url(args, pat: str, url: str) -> Dict:
    """
    Get the signed url to upload safely
    """
    req = requests.post(
        url=url + args.app_name + "/checkpointUrl", headers={"authorisation": pat}
    )
    signed_url = req.json()
    return signed_url
