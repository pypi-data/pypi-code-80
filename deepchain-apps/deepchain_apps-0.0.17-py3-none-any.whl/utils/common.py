"""Common functions for CLI module"""

import importlib
import json
import sys
from pathlib import Path
from typing import List

from .exceptions import AppNotFoundError, AppsNotFoundError


def get_app_info(app_name: str, kind="dir") -> str:
    """
    Get the directory of the application save in the deepchain config file
    """
    assert kind in ["dir", "status"], "Can on only select 'dir' or 'status'"

    path = Path.home().joinpath(".deep-chain").joinpath("apps")
    if not path.is_file():
        raise AppsNotFoundError

    with open(path, "r") as config_file:
        data = json.load(config_file)
        app_dir = data.get(app_name, None)

        if app_dir is None:
            raise AppNotFoundError(app_name)

        return app_dir[kind]


def get_scorer_configuration(app_name: str) -> List[str]:
    """
    Function to get the score_names of the scorer and regitrer it
    This function requires to load the module and get the score
    names via a @staticmethod
    """
    app_dir = get_app_info(app_name)
    app_dir = Path(app_dir)

    sys.path.append(str(app_dir.parent))
    mod = importlib.import_module(app_name + ".src.scorer")
    scores = mod.Scorer.score_names()
    # Remove last element of the path which was added manually
    sys.path.pop(-1)

    return scores


def _create_deechpain_folder() -> Path:
    """create .deepchain folder if not exist"""
    path = Path.home().joinpath(".deep-chain")
    path.mkdir(exist_ok=True)
    return path


def _create_config_file(root_path: Path) -> Path:
    """
    create the config file to store the personal access token
    """
    path = root_path.joinpath("config")
    path.touch(exist_ok=True)
    return path


def _create_apps_file(root_path: Path) -> Path:
    """
    create the apps file to store all the apps
    """
    path = root_path.joinpath("apps")
    path.touch(exist_ok=True)
    return path
