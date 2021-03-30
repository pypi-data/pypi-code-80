"""Operate the file
including read, write and find the latest file,
"""


# Local application imports
from crontip.linux_cmd import get_output


# Operate file
def find_latest_file(folder_path: str):
    """
    Return the name of latest file.
    """
    return get_output('ls -t {} | head -n 1'.format(folder_path))


def read_file(target: str):
    """
    Return a list of every lines in file.
    """
    with open(target, 'r') as stream:
        file = stream.readlines()
    return file


def write_file(
    data: list,
    save_folder: str = None, file_name: str = None,
    dest: str = None
) -> bool:
    """
    Write data into destination.
    """
    if dest is not None:
        try:
            with open(dest, mode='w') as stream:
                stream.write('\n'.join(data))
        except IsADirectoryError:
            print(f'{dest} is a directory, please use exact file name.')
            raise(SystemExit)
    else:
        with open(save_folder + file_name, 'w') as stream:
            stream.write('\n'.join(data))

    return True
