from pathlib import Path

from arkive.utility.audio import get_file_tags
from arkive.utility.folder import folder_files, file_move
from arkive.utility.sanitize import sanitize_path


def nest_music_file(file: Path, destination: Path):
    try:
        artist, album, title = get_file_tags(file)

        filepath = (destination / artist / album / title).with_suffix(file.suffix)
        output = sanitize_path(filepath)

        file_move(file, output)
    except AssertionError:
        pass


def nest_music_collection(origin: Path, destination: Path):
    for file in folder_files(origin):
        nest_music_file(file, destination)
