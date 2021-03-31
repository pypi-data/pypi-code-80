from pathlib import Path

from arkive.utility.audio import get_file_tags
from arkive.utility.folder import folder_files, folder_cleanup, file_move
from arkive.utility.sanitize import sanitize_path


def flat_music_file(file: Path, destination: Path):
    try:
        artist, album, title = get_file_tags(file)

        name = f'{artist} - {album} - {title}'
        filepath = (destination / name).with_suffix(file.suffix)
        output = sanitize_path(filepath)

        file_move(file, output)
    except AssertionError:
        pass


def flat_music_collection(origin: Path, destination: Path):
    for file in folder_files(origin, recurse=True):
        flat_music_file(file, destination)
    folder_cleanup(origin)
