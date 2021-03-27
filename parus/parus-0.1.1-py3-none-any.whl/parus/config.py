import configparser
import pathlib

from dataclasses import dataclass
from typing import Optional

CONFIG_DIR_NAME = '.parus'
CONFIG_FILE_NAME = 'parus.properties'
CREDENTIALS_FILE_NAME = 'credentials.json'
TOKEN_FILE_NAME = 'google-api-token.json'


def get_default_credentials_file():
    return pathlib.Path.home().joinpath(CONFIG_DIR_NAME, CREDENTIALS_FILE_NAME)


def token_file_for(credentials_file):
    return pathlib.Path(credentials_file).parent.joinpath(TOKEN_FILE_NAME)


def get_default_folder_id():
    c = Configuration.load(pathlib.Path.home() / CONFIG_DIR_NAME / CONFIG_FILE_NAME)
    return c.default.folder_id


@dataclass
class Properties:
    folder_id: Optional[str]

    @staticmethod
    def empty():
        return Properties(folder_id=None)


@dataclass
class Configuration:
    default: Optional[Properties]

    def save(self, f):
        cp = configparser.ConfigParser()
        cp['DEFAULT'] = self.default and self._to_properties_dict(self.default) or {}

        with open(f, 'w') as fp:
            cp.write(fp)

    def _to_properties_dict(self, p):
        return dict([(k.replace('_', '-'), v) for k, v in vars(p).items()
                     if v is not None])

    @staticmethod
    def load(f):
        if not pathlib.Path(f).exists():
            return Configuration(default=Properties.empty())

        cp = configparser.ConfigParser()
        with open(f) as fp:
            s = fp.read()
            cp.read_string(s)

        c = dict(cp)
        d = dict(c.pop('DEFAULT', {}))
        return Configuration(
            default=Properties(
                folder_id=d.get('folder-id', None)))
