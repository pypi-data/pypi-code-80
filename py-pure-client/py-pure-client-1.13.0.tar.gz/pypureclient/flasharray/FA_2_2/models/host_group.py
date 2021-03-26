# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_2 import models

class HostGroup(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'connection_count': 'int',
        'host_count': 'int',
        'is_local': 'bool',
        'space': 'Space'
    }

    attribute_map = {
        'name': 'name',
        'connection_count': 'connection_count',
        'host_count': 'host_count',
        'is_local': 'is_local',
        'space': 'space'
    }

    required_args = {
    }

    def __init__(
        self,
        name=None,  # type: str
        connection_count=None,  # type: int
        host_count=None,  # type: int
        is_local=None,  # type: bool
        space=None,  # type: models.Space
    ):
        """
        Keyword args:
            name (str): A user-specified name. The name must be locally unique and can be changed.
            connection_count (int): The number of volumes connected to the host group.
            host_count (int): The number of hosts in the host group.
            is_local (bool): Returns a value of `true` if the host or host group belongs to the current array. Returns a value of `false` if the host or host group belongs to a remote array.
            space (Space): Displays size and space consumption information.
        """
        if name is not None:
            self.name = name
        if connection_count is not None:
            self.connection_count = connection_count
        if host_count is not None:
            self.host_count = host_count
        if is_local is not None:
            self.is_local = is_local
        if space is not None:
            self.space = space

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `HostGroup`".format(key))
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
        if issubclass(HostGroup, dict):
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
        if not isinstance(other, HostGroup):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
