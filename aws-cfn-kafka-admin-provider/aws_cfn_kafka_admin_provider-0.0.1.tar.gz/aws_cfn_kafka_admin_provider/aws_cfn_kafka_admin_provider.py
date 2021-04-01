#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille <john@ews-network.net>


"""Main module."""

import re
import json
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from troposphere import Template
from troposphere import Ref, Sub
from troposphere import AWS_NO_VALUE

from aws_custom_ews_kafka_topic.custom import KafkaTopic as CTopic
from aws_custom_ews_kafka_topic.resource import KafkaTopic as RTopic


from .model import Topic, Model

NONALPHANUM = re.compile(r"([^a-zA-Z0-9]+)")


class KafkaStack(object):
    """
    Class to represent the Kafka topics / acls / schemas in CloudFormation.
    """

    def __init__(self, file_path):
        self.model = None
        self.template = Template("Kafka topics-acls-schemas root")
        self.stack = None
        self.topic_class = RTopic
        if file_path.endswith(".yaml") or file_path.endswith(".yml"):
            with open(file_path, "r") as file_fd:
                self.model = Model.parse_obj(yaml.load(file_fd.read(), Loader=Loader))
        else:
            self.model = Model.parse_file(file_path)

    def render_topics(self):
        function_name = None
        if self.model.FunctionName:
            self.topic_class = CTopic
            function_name = (
                function_name
                if self.model.FunctionName.startswith("arn:aws")
                else Sub(
                    f"arn:${{AWS::Partition}}:lambda:${{AWS::Region}}:${{AWS::AccountId}}:function:{function_name}"
                )
            )
        for topic in self.model.Topics:
            topic_cfg = topic.dict()
            if function_name:
                topic_cfg.update({"ServiceToken": function_name})
            topic_cfg.update(
                {
                    "BootstrapServers": self.model.BootstrapServers,
                    "SASLUsername": self.model.SASLUsername
                    if self.model.SASLUsername
                    else Ref(AWS_NO_VALUE),
                    "SASLPassword": self.model.SASLUsername
                    if self.model.SASLUsername
                    else Ref(AWS_NO_VALUE),
                    "SASLMechanism": self.model.SASLMechanism
                    if self.model.SASLUsername
                    else Ref(AWS_NO_VALUE),
                    "SecurityProtocol": self.model.SecurityProtocol
                    if self.model.SASLUsername
                    else Ref(AWS_NO_VALUE),
                }
            )
            if "Settings" in topic_cfg and not topic_cfg["Settings"]:
                del topic_cfg["Settings"]
            self.template.add_resource(
                self.topic_class(NONALPHANUM.sub("", topic.Name), **topic_cfg)
            )
