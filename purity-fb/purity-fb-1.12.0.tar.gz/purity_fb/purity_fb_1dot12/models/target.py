# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.12 Python SDK

    Pure Storage FlashBlade REST 1.12 Python SDK. Compatible with REST API versions 1.0 - 1.12. Developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.12
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Target(object):
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
        'id': 'str',
        'address': 'str',
        'ca_certificate_group': 'FixedReferenceWithId',
        'status': 'str',
        'status_details': 'str'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'address': 'address',
        'ca_certificate_group': 'ca_certificate_group',
        'status': 'status',
        'status_details': 'status_details'
    }

    def __init__(self, name=None, id=None, address=None, ca_certificate_group=None, status=None, status_details=None):  # noqa: E501
        """Target - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._id = None
        self._address = None
        self._ca_certificate_group = None
        self._status = None
        self._status_details = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if address is not None:
            self.address = address
        if ca_certificate_group is not None:
            self.ca_certificate_group = ca_certificate_group
        if status is not None:
            self.status = status
        if status_details is not None:
            self.status_details = status_details

    @property
    def name(self):
        """Gets the name of this Target.  # noqa: E501

        A name chosen by the user. Can be changed. Must be locally unique.  # noqa: E501

        :return: The name of this Target.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Target.

        A name chosen by the user. Can be changed. Must be locally unique.  # noqa: E501

        :param name: The name of this Target.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def id(self):
        """Gets the id of this Target.  # noqa: E501

        A non-modifiable, globally unique ID chosen by the system.  # noqa: E501

        :return: The id of this Target.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Target.

        A non-modifiable, globally unique ID chosen by the system.  # noqa: E501

        :param id: The id of this Target.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def address(self):
        """Gets the address of this Target.  # noqa: E501

        IP address or FQDN of the target system.  # noqa: E501

        :return: The address of this Target.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Target.

        IP address or FQDN of the target system.  # noqa: E501

        :param address: The address of this Target.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def ca_certificate_group(self):
        """Gets the ca_certificate_group of this Target.  # noqa: E501

        The group of CA certificates that can be used, in addition to well-known Certificate Authority certificates, in order to establish a secure connection to the target system. Defaults to a reference to the _default_replication_certs group.  # noqa: E501

        :return: The ca_certificate_group of this Target.  # noqa: E501
        :rtype: FixedReferenceWithId
        """
        return self._ca_certificate_group

    @ca_certificate_group.setter
    def ca_certificate_group(self, ca_certificate_group):
        """Sets the ca_certificate_group of this Target.

        The group of CA certificates that can be used, in addition to well-known Certificate Authority certificates, in order to establish a secure connection to the target system. Defaults to a reference to the _default_replication_certs group.  # noqa: E501

        :param ca_certificate_group: The ca_certificate_group of this Target.  # noqa: E501
        :type: FixedReferenceWithId
        """

        self._ca_certificate_group = ca_certificate_group

    @property
    def status(self):
        """Gets the status of this Target.  # noqa: E501

        Status of the connection. Valid values are connected and connecting. connected - The connection is OK. connecting - No connection exists and the array is trying to reconnect to the target.  # noqa: E501

        :return: The status of this Target.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Target.

        Status of the connection. Valid values are connected and connecting. connected - The connection is OK. connecting - No connection exists and the array is trying to reconnect to the target.  # noqa: E501

        :param status: The status of this Target.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def status_details(self):
        """Gets the status_details of this Target.  # noqa: E501

        Additional information describing any issues encountered when connecting, or null if the status is connected.  # noqa: E501

        :return: The status_details of this Target.  # noqa: E501
        :rtype: str
        """
        return self._status_details

    @status_details.setter
    def status_details(self, status_details):
        """Sets the status_details of this Target.

        Additional information describing any issues encountered when connecting, or null if the status is connected.  # noqa: E501

        :param status_details: The status_details of this Target.  # noqa: E501
        :type: str
        """

        self._status_details = status_details

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
        if issubclass(Target, dict):
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
        if not isinstance(other, Target):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
