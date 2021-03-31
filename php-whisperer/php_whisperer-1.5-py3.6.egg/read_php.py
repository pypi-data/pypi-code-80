"""
Tools for reading PHP arrays into python objects.
"""

import os, sys
from subprocess import check_output
import json


def read_many(*php_filenames, variable=None, include_path=None, cwd=".", modify_command=lambda x: x):
    command = modify_command(
        "\n".join(
            ["\n".join([
                f'echo json_encode(include "{x}");' 
                if not variable else
                f'if (file_exists("{x}")) @include "{x}";' for x in php_filenames]),
            f"echo json_encode(${variable});"])
    )
    if include_path:
        include_path = ["-d ", ",".join(include_path)]
    else:
        include_path = []
        with open('/tmp/php_whisperer_command', 'w') as wf:
            wf.write(command)
    result = check_output(['php']+include_path+['-r', command], cwd=cwd)
    return json.loads(result)

def alter_source_and_read_php(php_filename, *, 
        variable=None, 
        modify_command=lambda x: x, 
        alter_source=lambda x: x,
        debug=False,
        ):
    with open(php_filename, 'r') as rf:
        with open('/tmp/modphp.php', 'w') as wf:
            wf.write(alter_source(rf.read()))

    return read_php('/tmp/modphp.php', variable=variable, modify_command=modify_command, debug=debug)


def read_php(php_filename, *, variable=None, cwd=None, include_path=None, modify_command=lambda x: x, debug=False):
    """
    Given a php file denoted by the filename, return the array, or an array from the file.
    :type php_filename: str
    :type variable: str
    :return: list|dict
    """
    command = modify_command(
        f'echo json_encode(include "{php_filename}");' 
        if not variable else
        f'@include "{php_filename}"; echo json_encode(${variable});'
    )
    if include_path:
        include_path = ["-d ", ",".join(include_path)]
    else:
        include_path = []
    if debug:
        print(command)
        print(f"Include Path: {include_path}")
    result = check_output(['php']+include_path+['-r', command], cwd=cwd)
    return json.loads(result)

def combine_and_read(filenames, *, variable):
    """
    Given a list of php filenames, include them in the document and then capture the variable output.
    :type filenames: list
    :type variable: str
    :return: list|dict
    """
    initial_definition = '';
    result = check_output(['php', '-r', f'{initial_definition} ' + " ".join([
        '@include "{fn}";' for fn in filenames]) + ' echo json_encode(${variable});'])


def read_php_stdin():
    with open("/tmp/.php_out", "w") as wf:
        for x in sys.stdin:
            wf.write(x)

    if len(sys.argv) > 2:
        variable = sys.argv[1]
    else:
        variable = None
    print(read_php("/tmp/.php_out", variable=variable, debug="--debug" in sys.argv))

