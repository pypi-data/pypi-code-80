#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>

"""Definition of EWS::Kafka::Topic resource."""

from copy import deepcopy
from troposphere import AWSObject
from troposphere.validators import positive_integer, boolean

from aws_custom_ews_kafka_topic import COMMON_PROPS


class KafkaTopic(AWSObject):
    """
    Class to represent EWS::Kafka::Topic
    """

    resource_type = "EWS::Kafka::Topic"
    props = deepcopy(COMMON_PROPS)
