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
import ipaddress
import re
import time

import netifaces

# import collector module from parent directory
from digital_hydrant.collectors.collector import Collector
from digital_hydrant.config import config as conf


class Nmap(Collector):
    def __init__(self, name):
        super(Nmap, self).__init__(name)

    def run(self):
        iface = conf.get(self.name, "interface")
        ifaces = netifaces.interfaces()
        if iface not in ifaces:
            self.logger.error(f"Interface {iface} not available, exiting...")
            exit()
        else:
            self.logger.debug(f"Interface {iface} available")

        addrs = netifaces.ifaddresses(iface)[netifaces.AF_INET]
        if len(addrs) == 0:
            self.logger.error(f"No address available on interface {iface}, exiting...")
            exit()
        else:
            self.logger.debug(f"Address available on interface {iface}")

        addr = addrs[0]
        ip_addr = addr["addr"]
        subnet = addr["netmask"]

        net = str(ipaddress.ip_network(f"{ip_addr}/{subnet}", strict=False))

        # scan for hosts
        command = f"nmap -sn {net}"
        output = self.execute(command)

        timestamp = datetime.timestamp(datetime.now()) * 1000
        payload = self.__parse_output__(output)

        self.queue.put(
            **{"type": self.name, "payload": payload, "timestamp": timestamp}
        )

    def __parse_output__(self, output):
        # parse output into host list
        output = output.split("\n")
        hosts = []
        index = 0
        for entry in output:
            if "Nmap scan report" in entry:
                host = []
                host.append(entry)
                if "Host is up" in output[index + 1]:
                    host.append(output[index + 1])
                    if "MAC Address" in output[index + 2]:
                        host.append(output[index + 2])
                        hosts.append(host)

            index += 1

        for host in hosts:
            parsed_output = {}

            # find IP address
            ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", host[0]).group()

            parsed_output["ip"] = ip

            # perform a port scan
            command = f"nmap -sS {ip}"
            output = self.execute(command, timeout=60)

            parsed_output["scan_log"] = output.replace("\n", " ")

            # parse output into port list
            output = output.split("\n")
            port_list = []
            index = 0
            for entry in output:
                if "PORT" in entry:
                    index += 1
                    while True:
                        if "MAC Address" in output[index]:
                            break
                        else:
                            port_list.append(output[index])
                            index += 1

                index += 1

            port_string = ""
            for port in port_list:
                port = port.split(" ")
                port = port[0]
                port_string = port_string + str(port) + " "
            port_string = port_string[:-1]

            parsed_output["open_ports"] = port_string

        return parsed_output
