#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>

"""Definition of Custom::KafkaTopic."""

from copy import deepcopy
from troposphere.validators import positive_integer, boolean
from troposphere.cloudformation import AWSCustomObject

from aws_custom_ews_kafka_topic import COMMON_PROPS


class KafkaTopic(AWSCustomObject):
    """
    Class to represent EWS::Kafka::Topic
    """

    resource_type = "Custom::KafkaTopic"

    props = deepcopy(COMMON_PROPS)
    props.update(
        {
            "ServiceToken": (str, True),
        }
    )
