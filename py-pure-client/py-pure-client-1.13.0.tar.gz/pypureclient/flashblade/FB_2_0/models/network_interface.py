# coding: utf-8

"""
    FlashBlade REST API Client

    A lightweight client for FlashBlade REST API 2.0, developed by Pure Storage, Inc. (http://www.purestorage.com/).

    OpenAPI spec version: 2.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flashblade.FB_2_0 import models

class NetworkInterface(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'id': 'str',
        'address': 'str',
        'enabled': 'bool',
        'gateway': 'str',
        'mtu': 'int',
        'netmask': 'str',
        'services': 'list[str]',
        'subnet': 'object',
        'type': 'str',
        'vlan': 'int'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'address': 'address',
        'enabled': 'enabled',
        'gateway': 'gateway',
        'mtu': 'mtu',
        'netmask': 'netmask',
        'services': 'services',
        'subnet': 'subnet',
        'type': 'type',
        'vlan': 'vlan'
    }

    required_args = {
    }

    def __init__(
        self,
        name=None,  # type: str
        id=None,  # type: str
        address=None,  # type: str
        enabled=None,  # type: bool
        gateway=None,  # type: str
        mtu=None,  # type: int
        netmask=None,  # type: str
        services=None,  # type: List[str]
        subnet=None,  # type: object
        type=None,  # type: str
        vlan=None,  # type: int
    ):
        """
        Keyword args:
            name (str): Name of the object (e.g., a file system or snapshot).
            id (str): A non-modifiable, globally unique ID chosen by the system.
            address (str): The IPv4 or IPv6 address to be associated with the specified network interface.
            enabled (bool): Indicates if the specified network interface is enabled (`true`) or disabled (`false`). If not specified, defaults to `true`.
            gateway (str): Derived from `subnet.gateway`.
            mtu (int): Derived from `subnet.mtu`.
            netmask (str): Derived from `subnet.prefix`.
            services (list[str]): Services and protocols that are enabled on the interface.
            subnet (object)
            type (str): The only valid value is `vip`.
            vlan (int): Derived from `subnet.vlan`.
        """
        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if address is not None:
            self.address = address
        if enabled is not None:
            self.enabled = enabled
        if gateway is not None:
            self.gateway = gateway
        if mtu is not None:
            self.mtu = mtu
        if netmask is not None:
            self.netmask = netmask
        if services is not None:
            self.services = services
        if subnet is not None:
            self.subnet = subnet
        if type is not None:
            self.type = type
        if vlan is not None:
            self.vlan = vlan

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `NetworkInterface`".format(key))
        self.__dict__[key] = value

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if isinstance(value, Property):
            return None
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
        if issubclass(NetworkInterface, dict):
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
        if not isinstance(other, NetworkInterface):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
