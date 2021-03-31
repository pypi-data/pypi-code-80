import os
import harp_agent.settings as settings
import json
import errno
import pwd
import grp
from os.path import exists


def create_config_file():
    if exists(settings.PATH_TO_MS_CONFIG) is False:
        with open(settings.PATH_TO_MS_CONFIG, 'w+') as outfile:
            json.dump({}, outfile)


def create_folders():
    directories = ['/etc/harp-agent']
    uid = pwd.getpwnam("root").pw_uid
    gid = grp.getgrnam("root").gr_gid
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.chown(directory, uid, gid)


def prepare_service_for_first_start():
    create_folders()
    create_config_file()

