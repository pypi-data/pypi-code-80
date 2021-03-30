import importlib
import sys
from pathlib import Path

from deepchainapps import AppNotFoundError, ConfigNotFoundError
from deepchainapps.utils.common import get_app_dir


def _check_scorer_files(app_name: str):
    """
    Check if the name of the scorer has not been modified to be upload
    on the plateform
    """
    app_dir = Path(get_app_dir(app_name))

    if not app_dir.is_dir():
        raise AppNotFoundError(app_name)

    _check_init(app_dir)
    _check_init(app_dir.joinpath("src"))
    _check_scorer(app_dir.joinpath("src"))
    _check_module(app_dir, app_name)

    return


def _check_init(app_dir: Path) -> None:
    """Check if init file is in folder"""
    path_init = app_dir.joinpath("__init__.py")
    if not path_init.is_file():
        raise FileNotFoundError(
            "The app folder must be a module and contain __init__.py file"
        )


def _check_scorer(app_dir: Path) -> None:
    """Check if scorer file if in the app folder"""
    path_scorer = app_dir.joinpath("scorer.py")

    if not path_scorer.is_file():
        similar_file = _find_similar_file(app_dir, "score")
        message = "The scorer filename must be scorer.py"
        if similar_file is not None:
            message += f", found this similar file instead : {similar_file}"

        raise FileNotFoundError(message)


def _check_module(app_dir: Path, app_name: str) -> None:
    """Check if scorer module contains Score class"""
    # append current path to the pkg to find the app
    # as a module

    sys.path.append(str(app_dir.parent))
    mod = importlib.import_module(app_name + ".src.scorer")
    avail_members = dir(mod)
    sys.path.pop(-1)

    if "Scorer" not in avail_members:
        raise ModuleNotFoundError(
            "You must have a Scorer class in your scorer.py module"
        )


def _find_similar_file(path_folder: Path, pattern: str) -> str:
    """
    Find python files containing pattern in a specific folder
    """
    for file in path_folder.iterdir():
        filename = file.name
        if (filename.__contains__(pattern)) and (filename.endswith("py")):
            return filename
            break

    return None
