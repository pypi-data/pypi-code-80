#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>

"""Definition of Custom::KafkaTopic."""

from troposphere.validators import positive_integer, boolean
from troposphere.cloudformation import AWSCustomObject


class KafkaTopic(AWSCustomObject):
    """
    Class to represent EWS::Kafka::Topic
    """

    resource_type = "Custom::KafkaTopic"

    props = {
        "ServiceToken": (str, True),
        "Name": (str, True),
        "PartitionsCount": (positive_integer, True),
        "BootstrapServers": (str, True),
        "ReplicationFactor": (positive_integer, False),
        "SASLUsername": (str, False),
        "SASLPassword": (str, False),
        "IsConfluentKafka": (boolean, False),
    }
