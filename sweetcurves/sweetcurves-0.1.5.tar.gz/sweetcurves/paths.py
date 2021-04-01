from pathlib import Path
from typing import List, Optional

from loguru import logger
from toolz.curried import filter, first, map, pipe


def get_first_file(root: Path, matching: List[str] = []):
    assert matching, "The matching names must not be empty."
    found_file: Optional[Path] = pipe(
        root.glob("**/*"),
        filter(lambda _path: _path.is_file() and (_path.name in matching)),
        first)
    if not found_file:
        raise FileNotFoundError
    return found_file


def get_first_folder(root: Path, matching: List[str] = []):
    assert matching, "The matching names must not be empty."
    found_folder: Optional[Path] = pipe(
        root.glob("**/*"),
        filter(lambda _path: _path.is_file() and (_path.name in matching)),
        first)
    if not found_folder:
        raise FileNotFoundError("The folder you're looking for doesn't exist")
    return found_folder


def get_build_folder(root: Path) -> Path:
    build_folder = pipe(
        root.glob("**/*"),
        filter(lambda _path: _path.is_dir() and _path.name == "build"), first)
    if not build_folder:
        raise FileNotFoundError("The build folder doesn't exist")

    return build_folder


def get_docker_file(root: Path):
    build_directory: Path = get_build_folder(root)

    docker_file: Optional[Path] = get_first_file(
        build_directory, matching=["Dockerfile", "Dockerfile.dev"])

    if not docker_file:
        raise FileNotFoundError(
            "The Dockerfile we need to build doesn't exist.")
    return docker_file


def get_stack_settings(root: Path) -> Path:

    return get_first_file(root, ["stack.yml", "stack.yaml"])


def get_cloud_build(root: Path) -> Path:
    return get_first_file(root, matching=["cloudbuild.yml", "cloudbuild.yaml"])
