# -*-coding:utf8 -*
import shutil
import socket
import gettext
import os
_ = gettext.gettext

from makeitsoft import logger
from yaml import load

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """

    # ----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        """"""
        attrs = str([x for x in self.__dict__])
        return "<Dict2Obj: %s>" % attrs

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)



def load_file(conf_file_path):
    logger.info('Loading configuration file ' + conf_file_path + '...')
    with open(conf_file_path, 'rt', encoding='utf8') as yml:
        data = load(yml, Loader=Loader)
    logger.success('Configuration file loaded successfully')
    return data


def get_server_ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def change_language(targeted_locale):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    selected_language = gettext.translation('messages', localedir=os.path.join(base_dir, 'locales'), languages=[targeted_locale])
    selected_language.install()
    global _
    _ = selected_language.gettext


