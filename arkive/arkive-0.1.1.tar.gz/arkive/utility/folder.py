from pathlib import Path


def folder_files(folder: Path, recurse=False):
    glob = folder.rglob('*') if recurse else folder.glob('*')
    for item in glob:
        if item.is_file():
            yield item


def folder_remove(folder: Path):
    try:
        folder.rmdir()
    except OSError as err:
        print(err)


def folder_cleanup(folder: Path):
    for item in folder.glob("*"):
        if item.is_dir():
            folder_cleanup(item)
            folder_remove(item)


def file_move(file: Path, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)
    file.replace(output)
