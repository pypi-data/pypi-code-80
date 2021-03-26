# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_3 import models

class PodReplicaLinkPerformanceReplication(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'id': 'str',
        'bytes_per_sec_from_remote': 'int',
        'bytes_per_sec_to_remote': 'int',
        'bytes_per_sec_total': 'int',
        'direction': 'str',
        'local_pod': 'FixedReference',
        'remote_pod': 'FixedReference',
        'remotes': 'list[FixedReference]',
        'time': 'int'
    }

    attribute_map = {
        'id': 'id',
        'bytes_per_sec_from_remote': 'bytes_per_sec_from_remote',
        'bytes_per_sec_to_remote': 'bytes_per_sec_to_remote',
        'bytes_per_sec_total': 'bytes_per_sec_total',
        'direction': 'direction',
        'local_pod': 'local_pod',
        'remote_pod': 'remote_pod',
        'remotes': 'remotes',
        'time': 'time'
    }

    required_args = {
    }

    def __init__(
        self,
        id=None,  # type: str
        bytes_per_sec_from_remote=None,  # type: int
        bytes_per_sec_to_remote=None,  # type: int
        bytes_per_sec_total=None,  # type: int
        direction=None,  # type: str
        local_pod=None,  # type: models.FixedReference
        remote_pod=None,  # type: models.FixedReference
        remotes=None,  # type: List[models.FixedReference]
        time=None,  # type: int
    ):
        """
        Keyword args:
            id (str): A non-modifiable, globally unique ID chosen by the system.
            bytes_per_sec_from_remote (int): The number of bytes received per second from a remote array.
            bytes_per_sec_to_remote (int): The number of bytes transmitted per second to a remote array.
            bytes_per_sec_total (int): Total bytes transmitted and received per second.
            direction (str): The direction of replication. Valid values are `inbound` and `outbound`.
            local_pod (FixedReference): Reference to a local pod.
            remote_pod (FixedReference): Reference to a remote pod.
            remotes (list[FixedReference]): Reference to a remote array.
            time (int): Sample time in milliseconds since the UNIX epoch.
        """
        if id is not None:
            self.id = id
        if bytes_per_sec_from_remote is not None:
            self.bytes_per_sec_from_remote = bytes_per_sec_from_remote
        if bytes_per_sec_to_remote is not None:
            self.bytes_per_sec_to_remote = bytes_per_sec_to_remote
        if bytes_per_sec_total is not None:
            self.bytes_per_sec_total = bytes_per_sec_total
        if direction is not None:
            self.direction = direction
        if local_pod is not None:
            self.local_pod = local_pod
        if remote_pod is not None:
            self.remote_pod = remote_pod
        if remotes is not None:
            self.remotes = remotes
        if time is not None:
            self.time = time

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `PodReplicaLinkPerformanceReplication`".format(key))
        if key == "bytes_per_sec_from_remote" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `bytes_per_sec_from_remote`, must be a value greater than or equal to `0`")
        if key == "bytes_per_sec_to_remote" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `bytes_per_sec_to_remote`, must be a value greater than or equal to `0`")
        if key == "bytes_per_sec_total" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `bytes_per_sec_total`, must be a value greater than or equal to `0`")
        self.__dict__[key] = value

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if isinstance(value, Property):
            raise AttributeError
        else:
            return value

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            if hasattr(self, attr):
                value = getattr(self, attr)
                if isinstance(value, list):
                    result[attr] = list(map(
                        lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                        value
                    ))
                elif hasattr(value, "to_dict"):
                    result[attr] = value.to_dict()
                elif isinstance(value, dict):
                    result[attr] = dict(map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict") else item,
                        value.items()
                    ))
                else:
                    result[attr] = value
        if issubclass(PodReplicaLinkPerformanceReplication, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PodReplicaLinkPerformanceReplication):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
