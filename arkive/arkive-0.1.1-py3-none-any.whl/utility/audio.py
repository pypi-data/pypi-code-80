from pathlib import Path
from tinytag import TinyTag, TinyTagException

from arkive.utility.sanitize import sanitize_name


def get_file_tags(file: Path, sanitize=True):
    try:
        track = TinyTag.get(file)
        tags = (track.albumartist, track.album, track.title)
        if sanitize:
            tags = (sanitize_name(tag) for tag in tags)
        return tags
    except TinyTagException:
        raise AssertionError()
