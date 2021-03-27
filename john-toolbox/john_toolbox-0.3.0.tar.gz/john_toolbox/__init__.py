import toml
import os


def get_version():
    path = os.path.dirname(os.path.abspath("__file__")) + '/pyproject.toml'
    pyproject = toml.loads(open(str(path)).read())
    return pyproject['tool']['poetry']['version']


__version__ = get_version()
