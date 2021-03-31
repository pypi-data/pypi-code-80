from pathlib import Path

from arkive.utility.audio import get_file_tags
from arkive.utility.folder import folder_files


def show_music_file(file: Path):
    try:
        return get_file_tags(file, sanitize=False)
    except AssertionError:
        pass


def show_music_collection(origin: Path):
    content = []
    for file in folder_files(origin, recurse=True):
        item_row = show_music_file(file)
        if item_row:
            content.append(item_row)
    return ['ARTIST', 'ALBUM', 'TITLE'], content
