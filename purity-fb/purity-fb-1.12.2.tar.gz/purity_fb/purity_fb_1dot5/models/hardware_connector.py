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


class HardwareConnector(object):
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
        'connector_type': 'str',
        'lane_speed': 'int',
        'port_count': 'int',
        'transceiver_type': 'str'
    }

    attribute_map = {
        'name': 'name',
        'connector_type': 'connector_type',
        'lane_speed': 'lane_speed',
        'port_count': 'port_count',
        'transceiver_type': 'transceiver_type'
    }

    def __init__(self, name=None, connector_type=None, lane_speed=None, port_count=None, transceiver_type=None):  # noqa: E501
        """HardwareConnector - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._connector_type = None
        self._lane_speed = None
        self._port_count = None
        self._transceiver_type = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if connector_type is not None:
            self.connector_type = connector_type
        if lane_speed is not None:
            self.lane_speed = lane_speed
        if port_count is not None:
            self.port_count = port_count
        if transceiver_type is not None:
            self.transceiver_type = transceiver_type

    @property
    def name(self):
        """Gets the name of this HardwareConnector.  # noqa: E501

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :return: The name of this HardwareConnector.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this HardwareConnector.

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :param name: The name of this HardwareConnector.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def connector_type(self):
        """Gets the connector_type of this HardwareConnector.  # noqa: E501

        Form-factor of the interface. Valid values include QSFP and RJ-45.  # noqa: E501

        :return: The connector_type of this HardwareConnector.  # noqa: E501
        :rtype: str
        """
        return self._connector_type

    @connector_type.setter
    def connector_type(self, connector_type):
        """Sets the connector_type of this HardwareConnector.

        Form-factor of the interface. Valid values include QSFP and RJ-45.  # noqa: E501

        :param connector_type: The connector_type of this HardwareConnector.  # noqa: E501
        :type: str
        """

        self._connector_type = connector_type

    @property
    def lane_speed(self):
        """Gets the lane_speed of this HardwareConnector.  # noqa: E501

        Configured speed of each lane in the connector in bits-per-second  # noqa: E501

        :return: The lane_speed of this HardwareConnector.  # noqa: E501
        :rtype: int
        """
        return self._lane_speed

    @lane_speed.setter
    def lane_speed(self, lane_speed):
        """Sets the lane_speed of this HardwareConnector.

        Configured speed of each lane in the connector in bits-per-second  # noqa: E501

        :param lane_speed: The lane_speed of this HardwareConnector.  # noqa: E501
        :type: int
        """

        self._lane_speed = lane_speed

    @property
    def port_count(self):
        """Gets the port_count of this HardwareConnector.  # noqa: E501

        Configured number of ports in the connector. (1/2/4 for QSFP)  # noqa: E501

        :return: The port_count of this HardwareConnector.  # noqa: E501
        :rtype: int
        """
        return self._port_count

    @port_count.setter
    def port_count(self, port_count):
        """Sets the port_count of this HardwareConnector.

        Configured number of ports in the connector. (1/2/4 for QSFP)  # noqa: E501

        :param port_count: The port_count of this HardwareConnector.  # noqa: E501
        :type: int
        """

        self._port_count = port_count

    @property
    def transceiver_type(self):
        """Gets the transceiver_type of this HardwareConnector.  # noqa: E501

        Details about the transceiver which is plugged into the connector port. Transceiver type will be read-only for Pureuser. If nothing is plugged into QSFP port, value will be “Unused”. If a transceiver is plugged in, and type cannot be auto-detected,  and internal user has not specified a type - value will be “Unknown”. If transceiver is plugged in, and type is auto-detected, and/or type has been explicitly set by internal user - that value will be shown. Transceiver type is not applicable for RJ-45 connectors.  # noqa: E501

        :return: The transceiver_type of this HardwareConnector.  # noqa: E501
        :rtype: str
        """
        return self._transceiver_type

    @transceiver_type.setter
    def transceiver_type(self, transceiver_type):
        """Sets the transceiver_type of this HardwareConnector.

        Details about the transceiver which is plugged into the connector port. Transceiver type will be read-only for Pureuser. If nothing is plugged into QSFP port, value will be “Unused”. If a transceiver is plugged in, and type cannot be auto-detected,  and internal user has not specified a type - value will be “Unknown”. If transceiver is plugged in, and type is auto-detected, and/or type has been explicitly set by internal user - that value will be shown. Transceiver type is not applicable for RJ-45 connectors.  # noqa: E501

        :param transceiver_type: The transceiver_type of this HardwareConnector.  # noqa: E501
        :type: str
        """

        self._transceiver_type = transceiver_type

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
        if issubclass(HardwareConnector, dict):
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
        if not isinstance(other, HardwareConnector):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
