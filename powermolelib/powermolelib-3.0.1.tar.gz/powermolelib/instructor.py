#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File: instructor.py
#
# Copyright 2021 Vincent Schouten
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#

"""
Main code for instructor.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

from abc import ABC, abstractmethod
import socket
from socket import timeout
import os.path
from os.path import basename, dirname
from urllib.error import URLError
import urllib.request
import logging
import json
from voluptuous import Schema, Required, Any, MultipleInvalid

__author__ = '''Vincent Schouten <inquiry@intoreflection.co>'''
__docformat__ = '''google'''
__date__ = '''10-05-2019'''
__copyright__ = '''Copyright 2021, Vincent Schouten'''
__credits__ = ["Vincent Schouten"]
__license__ = '''MIT'''
__maintainer__ = '''Vincent Schouten'''
__email__ = '''<inquiry@intoreflection.co>'''
__status__ = '''Development'''  # "Prototype", "Development", "Production".

# This is the main prefix used for logging
LOGGER_BASENAME = '''Instructor'''
LOGGER = logging.getLogger(LOGGER_BASENAME)  # non-class objects like functions can consult this Logger object

# Constant for Pexpect. This prompt is default for Fedora and CentOS.
COMMAND_PROMPT = '[#$] '

# payload
HTTP_RESPONSE = Schema({Required("result"): Any(True, False)})


class Instructor(ABC):
    """Models an Instructor to interact with the Agent residing on target destination host.

    Note: As the Agent sits on top of target destination hosts' OS, many functions can be
    performed more effectively.

    """

    def __init__(self, group_ports):
        """Initializes the Instructor object."""
        logger_name = u'{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                                suffix=self.__class__.__name__)
        self._logger = logging.getLogger(logger_name)
        self.group_ports = group_ports
        self.host = '127.0.0.1'  # if-card of client
        self.socket_ = None

    def __str__(self):
        return 'Instructor'

    def _send_instruction(self, instruction):
        json_instruction = json.dumps(instruction)  # serialize dict to a JSON formatted str
        data = json_instruction.encode('utf-8')  # encode JSON formatted string to byte
        try:
            with urllib.request.urlopen(f'http://{self.host}:{self.group_ports["local_port_agent"]}',
                                        timeout=5,
                                        data=data) as request_obj:
                response_string = request_obj.read().decode('utf-8')  # from byte to string (JSON format)
            response_dict = json.loads(response_string)  # from JSON to dict
            response = HTTP_RESPONSE(response_dict)  # validating the structure of the content of an HTTP request
            result = response.get('result')
        except URLError:  # urllib.request.urlopen()
            self._logger.error('Agent could not be instructed. probable cause: '
                               'host unreachable or client has not connection to the Internet')
            result = False
        except ConnectionResetError:  # urllib.request.urlopen()
            self._logger.error('something went wrong: connection is reset by Agent')
            result = False
        except timeout:  # urllib.request.urlopen()
            LOGGER.error('Agent could not be instructed. probably cause: '
                         'timeout exceeded for the connection attempt')
            result = False
        except json.decoder.JSONDecodeError:  # json.loads()
            self._logger.error('response of Agent could not be read, '
                               'JSON document could not be deserialized')
            result = False
        except MultipleInvalid:  # HTTP_RESPONSE()
            self._logger.error('response of Agent could not be read. '
                               'data structure validating failed ("MultipleInvalid")')
            result = False
        return result

    def _start_heartbeat_responder(self, host_port):
        """Sends the instruction to Agent to start the heartbeat responder."""
        return self._start_server(host_port, 'heartbeat_responder_start', 'heartbeat responder')

    def _start_command_server(self, host_port):
        """Starts the command server."""
        return self._start_server(host_port, 'command_server_start', 'command server')

    def _start_transfer_server(self, host_port):
        """Starts the transfer server."""
        return self._start_server(host_port, 'transfer_server_start', 'transfer server')

    def _start_server(self, host_port, process, message):
        """Starts the transfer server."""
        self._logger.debug('instructing Agent to start %s', message)
        result = self._send_instruction({'process': process,
                                         'arguments': {'local_port': host_port}})
        self._logger.debug('Agent responded with: %s', result)
        return result

    # def start_agent(self):
    #     print("the BootstrapAgent-module is responsible for starting agent.py (Agent) on destination host")

    def stop_agent(self):
        """Starts the Agent on destination host."""
        self._logger.debug('instructing Agent to stop itself')
        result = self._send_instruction({'process': 'stop',
                                         'arguments': {}})
        self._logger.debug('Agent responded with: %s', result)
        return result

    def send_command(self, command):
        """Executes Linux command and returns the response in a byte list."""
        if command.lower().strip() == 'exit':
            response = [b'ABORTED: hit control + c to end interactive mode']
            return response
        try:
            command_json = json.dumps({'command': command})  # serialize dict to a JSON formatted str
            command_byte = command_json.encode('utf-8')  # encode JSON formatted string to byte
            with urllib.request.urlopen(f'http://{self.host}:{self.group_ports["local_port_command"]}',
                                        timeout=5, data=command_byte) as request_obj:
                # response = request_obj.read().decode('utf-8')  # from byte to string
                response = request_obj.read()
        except URLError:
            self._logger.error('URLError. '
                               'HTTP request could not be send over forwarded connection to Agent. '
                               'probable cause: host unreachable or client has not connection to the Internet')
            response = False
        except ConnectionResetError:
            self._logger.error('ConnectionResetError. '
                               'HTTP request could not be send over forwarded connection to Agent. '
                               'probable cause: Agent not bind to port')
            response = False
        except timeout:
            LOGGER.error('HTTP request could not be send over forwarded connection to Agent. '
                         'timeout exceeded for the connection attempt. '
                         'probable cause: host unreachable or client has not connection to the Internet')
            response = False
        return response

    def send_file(self, path_file_source, path_destination):
        """Opens the sockets and connects to transfer server (ie. Agent) and sends a file."""
        data_protocol = DataProtocol()
        file_name = basename(path_file_source)
        path_src = dirname(path_file_source)
        path_dst = path_destination
        self.socket_ = socket.socket()
        self.socket_.connect(('localhost', self.group_ports["local_port_transfer"]))
        self._logger.debug('connection from client to transfer server by Agent on destination host established')
        try:
            path_dst_bin = data_protocol.path_dst(path_dst=path_dst)
            file_name_bin = data_protocol.file_name(file_name=file_name)
            file_size_bin = data_protocol.file_size(path_src=path_src, file_name=file_name)
            self._send_file(path_src=path_src,
                            file_name=file_name,
                            file_name_bin=file_name_bin,
                            file_size_bin=file_size_bin,
                            path_dst_bin=path_dst_bin)
            self._logger.info('file %s is transferred', path_file_source)
        except FileNotFoundError:
            self._logger.error('file or directory is requested but does not exist')
        finally:
            self.socket_.close()
        return True

    def _send_file(self,  # pylint: disable=too-many-arguments
                   path_src,
                   file_name,
                   file_name_bin,
                   file_size_bin,
                   path_dst_bin):
        metadata = path_dst_bin + file_name_bin + file_size_bin  # type is "bytes"
        path_to_file = os.path.join(path_src, file_name)
        self._logger.debug('sending file name, file size and file content')
        data = open(path_to_file, 'rb')  # type is "_io.BufferedReader"
        self.socket_.sendall(metadata + data.read())

    @abstractmethod
    def start(self):
        """Starts the necessary programs on target destination host."""

    @abstractmethod
    def stop(self):
        """Terminates the started program(s) and the Agent on target destination host."""


class ForInstructor(Instructor):
    """Provides interaction with the Agent, which resides on target destination host, to accommodate FOR mode.

    Functions:
    - forwards connections (FOR) implicitly, because SSH is responsible for forwarding connections, not the Agent
    - interaction with the heartbeat responder
    - provide access to OS services (COMMAND)
    - transfer files (TRANSFER)
    """

    def __init__(self, group_ports):
        """Initializes the ForInstructor object.

        Args:
            group_ports (dict): A group of ports for powermole to bind on (localhost and target destination host)

        """
        Instructor.__init__(self, group_ports)

    def start(self):
        """Starts the heartbeat responder."""
        return all([self._start_heartbeat_responder(host_port=self.group_ports["remote_port_heartbeat"]),
                    self._start_command_server(host_port=self.group_ports["remote_port_command"]),
                    self._start_transfer_server(host_port=self.group_ports["remote_port_transfer"])])

    def stop(self):
        """Terminates the Agent on destination host and started services (heartbeat responder, command server, etc)."""
        return self.stop_agent()


class TorInstructor(Instructor):
    """Provides interaction with the Agent, which resides on target destination host, to accommodate Tor mode.

    Functions:
    - proxify internet traffic (TOR)
    - interaction with the heartbeat responder
    - provide access to OS services (COMMAND)
    - transfer files (TRANSFER)
    """

    def __init__(self, group_ports, ip_address_i, ip_address_e):
        """Initializes the TorInstructor object.

        Args:
            group_ports (dict): A group of ports for powermole to bind on (localhost and target destination host)
            ip_address_i (basestring): The IP address on host for incoming SOCKS encapsulated connections.
            ip_address_e (basestring): The IP address on host (on a possible different ifcard) for outgoing connections.

        """
        Instructor.__init__(self, group_ports)
        self.ip_address_i = ip_address_i
        self.ip_address_e = ip_address_e

    def _start_proxy_server(self, remote_address_i, remote_port_i, remote_address_e):
        """Sends an instruction to Agent to start the proxy server."""
        self._logger.debug('instructing Agent to start the proxy server')
        result = self._send_instruction({'process': 'proxy_server_start',
                                         'arguments': {'remote_address_i': remote_address_i,
                                                       'remote_port_i': remote_port_i,
                                                       'remote_address_e': remote_address_e}})
        self._logger.debug('Agent responded with: %s', result)
        return result

    def start(self):
        """Starts the SOCKS proxy and heartbeat responder."""
        return all([self._start_proxy_server(remote_address_i=self.ip_address_i,
                                             remote_port_i=self.group_ports["remote_port_proxy"],
                                             remote_address_e=self.ip_address_e),
                    self._start_heartbeat_responder(host_port=self.group_ports["remote_port_heartbeat"]),
                    self._start_command_server(host_port=self.group_ports["remote_port_command"]),
                    self._start_transfer_server(host_port=self.group_ports["remote_port_transfer"])])

    def stop(self):
        """Terminates the Agent on destination host and all started services (heartbeat responder, proxy server, ..)."""
        return self.stop_agent()


class PlainInstructor(Instructor):
    """Provides interaction with the Agent, which resides on target destination host, to accommodate FOR mode.

    Functions:
    - interaction with the heartbeat responder
    - provide access to OS services (COMMAND)
    - transfer files (TRANSFER)
    """

    def __init__(self, group_ports):
        """Initializes the ForInstructor object.

        Args:
            group_ports (dict): A group of ports for powermole to bind on (localhost and target destination host)

        """
        Instructor.__init__(self, group_ports)

    def start(self):
        """Starts the heartbeat responder."""
        return all([self._start_heartbeat_responder(host_port=self.group_ports["remote_port_heartbeat"]),
                    self._start_command_server(host_port=self.group_ports["remote_port_command"]),
                    self._start_transfer_server(host_port=self.group_ports["remote_port_transfer"])])

    def stop(self):
        """Terminates the Agent on destination host and started services (heartbeat responder, command server, etc)."""
        return self.stop_agent()


class DataProtocol:
    """Encodes file metadata to a binary format."""

    def __init__(self):
        logger_name = u'{base}.{suffix}'.format(base=LOGGER_BASENAME,
                                                suffix='DataProtocol')
        self._logger = logging.getLogger(logger_name)

    def path_dst(self, path_dst):
        """Encodes the destination path."""
        self._logger.debug('path to directory on remote server: %s', path_dst)
        length_path_int = len(path_dst)
        length_path_bin = bin(length_path_int)[2:].zfill(16)  # (str) from decimal to binary (eg. 0000000000001110)
        return length_path_bin.encode('utf-8') + path_dst.encode('utf-8')  # binary

    def file_name(self, file_name):
        """Encodes (only) the file name - not the directory."""
        self._logger.debug('name of file to be transferred: %s', file_name)
        length_file_int = len(file_name)
        length_file_bin = bin(length_file_int)[2:].zfill(16)  # (str) from dec to bin + pad with zeros to fill w=16b
        return length_file_bin.encode('utf-8') + file_name.encode('utf-8')  # (binary)

    def file_size(self, path_src, file_name):
        """Encodes the file size."""
        path_to_file = os.path.join(path_src, file_name)
        size_file_int = os.path.getsize(path_to_file)
        self._logger.debug('size of file %s: %s bytes', file_name, size_file_int)
        size_file_bin = bin(size_file_int)[2:].zfill(32)  # (str) from dec to bin + pad with zeros to fill width of 32b
        return size_file_bin.encode('utf-8')
