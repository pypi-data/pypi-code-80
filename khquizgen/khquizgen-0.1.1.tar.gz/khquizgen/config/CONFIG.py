import os
from pathlib import Path
import configparser

config = configparser.ConfigParser()
uc = Path(__file__).resolve().parent.joinpath('config.ini')
if uc.exists():
    config.read(uc)
else:
    config['DEFAULT'] = {}


# Choose verbosity of output
if os.getenv('DEBUG_APP'):
    DEBUG = True
else:
    DEBUG = False


def get_inputs_path(pkg_root):
    path = Path(config['DEFAULT'].get('Input', pkg_root))
    return path.joinpath('inputs')


def get_outputs_path(pkg_root):
    path = Path(config['DEFAULT'].get('Output', pkg_root))
    return path.joinpath('outputs')


def get_log_path(pkg_root):
    path = Path(config['DEFAULT'].get('Logs', Path(pkg_root.parent)))
    return path.joinpath('logs', 'answer.log')
