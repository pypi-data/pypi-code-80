# Copyright 2021 Outside Open
# This file is part of Digital-Hydrant.

# Digital-Hydrant is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Digital-Hydrant is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Digital-Hydrant.  If not, see https://www.gnu.org/licenses/.

from configparser import ConfigParser
import os
import pkg_resources

ini_path = (
    "/etc/digital-hydrant/config.ini"
    if not "DH_CONFIG" in os.environ
    else os.environ.get("DH_CONFIG")
)
db_path = (
    "/var/lib/digital-hydrant/digital-hydrant.db"
    if not "DH_DATABASE" in os.environ
    else os.environ.get("DH_DATABASE")
)

config = ConfigParser()
config["global"] = {"logfile": "/var/log/digital-hydrant.log"}

config["api"] = {
    "token": "",
}

config["logging"] = {
    "level": "DEBUG",
}

config["hydra"] = {
    "wordlist_path": pkg_resources.resource_filename(
        "digital_hydrant", "config/hydra/wordlist.txt"
    ),
    "userlist_path": pkg_resources.resource_filename(
        "digital_hydrant", "config/hydra/userlist.txt"
    ),
    "snmp_wordlist_path": pkg_resources.resource_filename(
        "digital_hydrant", "config/hydra/snmp_wordlist.txt"
    ),
    "interface": "eth0",
}

config["netdiscover"] = {
    "exec_duration": 60,
}

config["nmap"] = {
    "interface": "eth0",
}

config["vlan"] = {
    "interface": "eth0",
}

config["wifi_auth"] = {"exec_duration": 30}

config["wifi_quality"] = {"exec_time": 10, "interface": "wlan0"}

config["ping"] = {"wait": 180}

if os.path.isfile(ini_path):
    config.read(ini_path)
else:
    default_ini_path = pkg_resources.resource_filename(
        "digital_hydrant", "config/config.ini"
    )

    config.read(default_ini_path)

    os.makedirs(os.path.dirname(ini_path), exist_ok=True)
    with open(ini_path, "w") as configfile:
        config.write(configfile)

if not os.path.isfile(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with open(db_path, "w") as configfile:
        pass


def get_sections(start):
    values = []
    for section in config.sections():
        if section.startswith(start):
            values.append(section)

    return values


def update_config(data, path=ini_path):
    changes = False
    for section, value in data.items():
        if (
            isinstance(value, dict)
            and section in config.sections()
            and config[section] != value
        ):
            config[section] = value
            changes = True

    if changes:
        with open(path, "w") as configfile:
            config.write(configfile)
