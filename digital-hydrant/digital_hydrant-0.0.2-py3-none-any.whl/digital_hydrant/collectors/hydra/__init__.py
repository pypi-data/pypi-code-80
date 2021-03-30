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

import re
import time
import importlib
from datetime import datetime, timedelta

from digital_hydrant.collectors.collector import Collector
import digital_hydrant.config

from netifaces import AF_INET, ifaddresses
import sqlite3


class Hydra(Collector):
    def __init__(self, name):
        super(Hydra, self).__init__(name)

        try:
            self.table_name = "unique_ips"
            self.conn = sqlite3.connect(digital_hydrant.config.db_path)
            self.cursor = self.conn.cursor()

            columns = "id INTEGER PRIMARY KEY AUTOINCREMENT, ip TEXT UNIQUE, last_tested TIMESTAMP"
            self.cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns})"
            )
        except Exception as err:
            self.logger.critical(f"Failed to initialize database for Hydra: {err}")

    def run(self):
        week_ago = datetime.timestamp(datetime.now() - timedelta(weeks=1)) * 1000
        self.cursor.execute(
            f"SELECT ip FROM unique_ips WHERE last_tested IS NULL or last_tested < {week_ago} ORDER BY last_tested ASC"
        )

        records = self.cursor.fetchall()
        for record in records:
            self.__hydra__(record[0])

    def __hydra__(self, ip):
        importlib.reload(digital_hydrant.config)
        ssh_enabled = digital_hydrant.config.config.getboolean(
            self.name, "enable_ssh", fallback=True
        )
        snmp_enabled = digital_hydrant.config.config.getboolean(
            self.name, "enable_snmp", fallback=True
        )

        if not (ssh_enabled or snmp_enabled):
            return

        iface = digital_hydrant.config.config.get(self.name, "interface")

        # connect to subnet, use X.X.X.227 because it is rarely used
        my_subnet_ip = "{}.227".format(re.sub(r"\.\d+$", "", ip))
        self.logger.debug(f"Joining {ip} network, with IP {my_subnet_ip}")
        self.execute(f"ifconfig {iface}:1 {my_subnet_ip}")

        userlist_path = digital_hydrant.config.config.get(self.name, "userlist_path")
        wordlist_path = digital_hydrant.config.config.get(self.name, "wordlist_path")
        snmp_wordlist_path = digital_hydrant.config.config.get(
            self.name, "snmp_wordlist_path"
        )

        parsed_output = {}
        parsed_output["target"] = ip

        ssh_output = ""
        snmp_output = ""

        if ssh_enabled:
            ssh_command = (
                f"hydra -I -L {userlist_path} -P {wordlist_path} {ip} ssh 2>&1"
            )
            ssh_output = self.execute(ssh_command)

            parsed_output["ssh"] = self.parse_output(ssh_output)
            parsed_output["ssh_output_log"] = ssh_output

        if snmp_enabled:
            snmp_command = f"hydra -I -P {snmp_wordlist_path} {ip} snmp 2>&1"
            snmp_output = self.execute(snmp_command)

            parsed_output["snmp"] = self.parse_output(snmp_output)
            parsed_output["snmp_output_log"] = snmp_output

        parsed_output["vulnerable"] = (
            ssh_enabled and parsed_output["ssh"]["vulnerable"]
        ) or (snmp_enabled and parsed_output["snmp"]["vulnerable"])

        timestamp = datetime.timestamp(datetime.now()) * 1000

        self.queue.put(
            **{"type": self.name, "payload": parsed_output, "timestamp": timestamp}
        )

        # disconnect from subnet
        self.logger.debug(f"Disconnecting from {ip}")
        self.execute(f"ifconfig {iface}:1 down")

        try:
            self.cursor.execute(
                f"UPDATE {self.table_name} SET last_tested={timestamp} WHERE ip='{ip}'"
            )
        except sqlite3.Error as e:
            self.logger.error(f"Failed to update last_tested for {ip}: {e}")
        finally:
            self.conn.commit()

    def parse_output(self, output):
        data = {}
        results = []
        for line in output.split("\n"):
            if not line.strip():
                continue

            if line.startswith("[DATA]"):
                for part in line.split(","):
                    if "login tries" in part:
                        temp = re.findall(r"\d+", part)
                        res = list(map(int, temp))
                        data["login_tries"] = res[0]
                        data["usernames_tested"] = res[1]
                        data["passwords_tested"] = res[2]
            elif line.startswith("1 of 1"):
                for part in line.split(","):
                    if "valid password" in part:
                        temp = re.findall(r"\d+", part)
                        res = list(map(int, temp))
                        data["successful_logins"] = res[0]
            elif line.startswith("[22][ssh]") or line.startswith("[161][snmp]"):
                parts = line.split()
                result = {}
                for i in range(1, len(parts), 2):
                    result[parts[i].replace(":", "")] = parts[i + 1]
                results.append(result)

        data["results"] = results
        data["vulnerable"] = len(results) > 0

        return data
