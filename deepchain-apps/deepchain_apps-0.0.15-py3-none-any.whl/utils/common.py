"""Common functions for CLI module"""

import importlib
import json
import sys
from pathlib import Path
from typing import List

from .exceptions import AppNotFoundError


def get_app_dir(app_name: str) -> str:
    """
    Get the directory of the application save in the deepchain config file
    """
    path = Path.home().joinpath(".deep-chain").joinpath("config")
    with open(path, "r") as config_file:
        data = json.load(config_file)
        app_dir = data.get(app_name, None)

        if app_dir is None:
            raise AppNotFoundError(app_name)

        return app_dir["dir"]


def get_scorer_configuration(app_name: str) -> List[str]:
    """
    Function to get the score_names of the scorer and regitrer it
    This function requires to load the module and get the score
    names via a @staticmethod
    """
    app_dir = get_app_dir(app_name)
    app_dir = Path(app_dir)

    sys.path.append(str(app_dir.parent))
    mod = importlib.import_module(app_name + ".scorer")
    scores = mod.Scorer.score_names()
    # Remove last element of the path which was added manually
    sys.path.pop(-1)

    return scores
