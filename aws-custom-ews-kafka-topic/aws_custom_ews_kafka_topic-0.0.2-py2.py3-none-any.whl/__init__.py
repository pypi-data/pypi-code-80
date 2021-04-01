#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>

"""Top-level package for Kafka::Topic."""


from troposphere import AWSProperty
from troposphere.validators import positive_integer, boolean


__author__ = """John Mille"""
__email__ = "john@ews-network.net"
__version__ = "0.0.2"


COMMON_PROPS = {
    "Name": (str, True),
    "PartitionsCount": (positive_integer, True),
    "BootstrapServers": (str, True),
    "ReplicationFactor": (positive_integer, False),
    "SecurityProtocol": (str, False),
    "SASLMechanism": (str, False),
    "SASLUsername": (str, False),
    "SASLPassword": (str, False),
    "IsConfluentKafka": (boolean, False),
    "Settings": (dict, False)
}
