# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.5 Python SDK

    Pure Storage FlashBlade REST 1.5 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.5
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class NetworkInterface(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

#BEGIN_CUSTOM
    # IR-51527: Prevent Pytest from attempting to collect this class based on name.
    __test__ = False
#END_CUSTOM

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'name': 'str',
        'address': 'str',
        'enabled': 'bool',
        'gateway': 'str',
        'mtu': 'int',
        'netmask': 'str',
        'services': 'list[str]',
        'type': 'str',
        'vlan': 'int'
    }

    attribute_map = {
        'name': 'name',
        'address': 'address',
        'enabled': 'enabled',
        'gateway': 'gateway',
        'mtu': 'mtu',
        'netmask': 'netmask',
        'services': 'services',
        'type': 'type',
        'vlan': 'vlan'
    }

    def __init__(self, name=None, address=None, enabled=None, gateway=None, mtu=None, netmask=None, services=None, type=None, vlan=None):  # noqa: E501
        """NetworkInterface - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._address = None
        self._enabled = None
        self._gateway = None
        self._mtu = None
        self._netmask = None
        self._services = None
        self._type = None
        self._vlan = None
        self.discriminator = None

        if name is not None:
            self.name = name
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
        if type is not None:
            self.type = type
        if vlan is not None:
            self.vlan = vlan

    @property
    def name(self):
        """Gets the name of this NetworkInterface.  # noqa: E501

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :return: The name of this NetworkInterface.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this NetworkInterface.

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :param name: The name of this NetworkInterface.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def address(self):
        """Gets the address of this NetworkInterface.  # noqa: E501


        :return: The address of this NetworkInterface.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this NetworkInterface.


        :param address: The address of this NetworkInterface.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def enabled(self):
        """Gets the enabled of this NetworkInterface.  # noqa: E501

        Indicates if subnet is enabled (true) or disabled (false). Enabled by default.  # noqa: E501

        :return: The enabled of this NetworkInterface.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this NetworkInterface.

        Indicates if subnet is enabled (true) or disabled (false). Enabled by default.  # noqa: E501

        :param enabled: The enabled of this NetworkInterface.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def gateway(self):
        """Gets the gateway of this NetworkInterface.  # noqa: E501


        :return: The gateway of this NetworkInterface.  # noqa: E501
        :rtype: str
        """
        return self._gateway

    @gateway.setter
    def gateway(self, gateway):
        """Sets the gateway of this NetworkInterface.


        :param gateway: The gateway of this NetworkInterface.  # noqa: E501
        :type: str
        """

        self._gateway = gateway

    @property
    def mtu(self):
        """Gets the mtu of this NetworkInterface.  # noqa: E501

        Maximum message transfer unit (packet) size for the subnet in bytes. MTU setting cannot exceed the MTU of the corresponding physical interface. 1500 by default.  # noqa: E501

        :return: The mtu of this NetworkInterface.  # noqa: E501
        :rtype: int
        """
        return self._mtu

    @mtu.setter
    def mtu(self, mtu):
        """Sets the mtu of this NetworkInterface.

        Maximum message transfer unit (packet) size for the subnet in bytes. MTU setting cannot exceed the MTU of the corresponding physical interface. 1500 by default.  # noqa: E501

        :param mtu: The mtu of this NetworkInterface.  # noqa: E501
        :type: int
        """

        self._mtu = mtu

    @property
    def netmask(self):
        """Gets the netmask of this NetworkInterface.  # noqa: E501


        :return: The netmask of this NetworkInterface.  # noqa: E501
        :rtype: str
        """
        return self._netmask

    @netmask.setter
    def netmask(self, netmask):
        """Sets the netmask of this NetworkInterface.


        :param netmask: The netmask of this NetworkInterface.  # noqa: E501
        :type: str
        """

        self._netmask = netmask

    @property
    def services(self):
        """Gets the services of this NetworkInterface.  # noqa: E501


        :return: The services of this NetworkInterface.  # noqa: E501
        :rtype: list[str]
        """
        return self._services

    @services.setter
    def services(self, services):
        """Sets the services of this NetworkInterface.


        :param services: The services of this NetworkInterface.  # noqa: E501
        :type: list[str]
        """

        self._services = services

    @property
    def type(self):
        """Gets the type of this NetworkInterface.  # noqa: E501

        Possible values are vip.  # noqa: E501

        :return: The type of this NetworkInterface.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this NetworkInterface.

        Possible values are vip.  # noqa: E501

        :param type: The type of this NetworkInterface.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def vlan(self):
        """Gets the vlan of this NetworkInterface.  # noqa: E501


        :return: The vlan of this NetworkInterface.  # noqa: E501
        :rtype: int
        """
        return self._vlan

    @vlan.setter
    def vlan(self, vlan):
        """Sets the vlan of this NetworkInterface.


        :param vlan: The vlan of this NetworkInterface.  # noqa: E501
        :type: int
        """

        self._vlan = vlan

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
