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

from datetime import datetime
import subprocess
import time

from digital_hydrant.collectors.collector import Collector


class Netdiscover(Collector):
    def __init__(self, name):
        super(Netdiscover, self).__init__(name)

    def run(self):
        command = f"timeout {self.exec_duration} netdiscover -N -P"
        self.logger.debug(f"Command: {command}")
        self.logger.debug("Broadcasting to 255.255.255.255 network")
        broadcast_proc = subprocess.Popen(
            "ping -b 255.255.255.255 2>&1", shell=True, stdout=subprocess.PIPE
        )
        output = self.execute(command)
        broadcast_proc.kill()

        timestamp = datetime.timestamp(datetime.now()) * 1000
        all_output = self.__parse_output__(output.split("\n"))

        for payload in all_output:
            self.queue.put(
                **{"type": self.name, "payload": payload, "timestamp": timestamp}
            )

    def __parse_output__(self, output):
        cleaned_data = []
        for i in output:
            parsed_output = {}
            parts = i.split(" ")
            parts = list(filter(("").__ne__, parts))

            if len(parts) < 5:
                continue

            # IP Adress
            parsed_output["ip"] = parts[0]

            # MAC Address
            parsed_output["mac_address"] = parts[1]

            # Hostname
            name = ""
            max_index = len(parts)
            for ii in range(4, max_index):
                name += parts[ii] + " "
            if name != "":
                name = name[:-1]
            parsed_output["hostname"] = name

            cleaned_data.append(parsed_output)

        return cleaned_data
