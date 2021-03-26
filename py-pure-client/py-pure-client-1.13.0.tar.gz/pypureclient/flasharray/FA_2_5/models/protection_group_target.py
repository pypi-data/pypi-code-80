# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.5
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_5 import models

class ProtectionGroupTarget(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'protection_group': 'ReferenceNoId',
        'target': 'ReferenceNoId',
        'allowed': 'bool'
    }

    attribute_map = {
        'protection_group': 'protection_group',
        'target': 'target',
        'allowed': 'allowed'
    }

    required_args = {
    }

    def __init__(
        self,
        protection_group=None,  # type: models.ReferenceNoId
        target=None,  # type: models.ReferenceNoId
        allowed=None,  # type: bool
    ):
        """
        Keyword args:
            protection_group (ReferenceNoId)
            target (ReferenceNoId)
            allowed (bool): If set to `true`, the target array has allowed the source array to replicate protection group data to the target array. If set to `false`, the target array has not allowed the source array to replicate protection group data to the target.
        """
        if protection_group is not None:
            self.protection_group = protection_group
        if target is not None:
            self.target = target
        if allowed is not None:
            self.allowed = allowed

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `ProtectionGroupTarget`".format(key))
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
        if issubclass(ProtectionGroupTarget, dict):
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
        if not isinstance(other, ProtectionGroupTarget):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
