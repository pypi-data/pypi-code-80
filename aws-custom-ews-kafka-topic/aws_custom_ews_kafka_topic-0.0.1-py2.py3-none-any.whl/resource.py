#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>

"""Definition of EWS::Kafka::Topic resource."""

from troposphere import AWSObject
from troposphere.validators import positive_integer, boolean


class KafkaTopic(AWSObject):
    """
    Class to represent EWS::Kafka::Topic
    """

    resource_type = "EWS::Kafka::Topic"

    props = {
        "Name": (str, True),
        "PartitionsCount": (positive_integer, True),
        "BootstrapServers": (str, True),
        "ReplicationFactor": (positive_integer, False),
        "SASLUsername": (str, False),
        "SASLPassword": (str, False),
        "IsConfluentKafka": (boolean, False),
    }
