# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.11 Python SDK

    Pure Storage FlashBlade REST 1.11 Python SDK. Compatible with REST API versions 1.0 - 1.11. Developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.11
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class SyslogServerSetting(object):
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
        'ca_certificate': 'Reference',
        'ca_certificate_group': 'Reference'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'ca_certificate': 'ca_certificate',
        'ca_certificate_group': 'ca_certificate_group'
    }

    def __init__(self, name=None, id=None, ca_certificate=None, ca_certificate_group=None):  # noqa: E501
        """SyslogServerSetting - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._id = None
        self._ca_certificate = None
        self._ca_certificate_group = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if ca_certificate is not None:
            self.ca_certificate = ca_certificate
        if ca_certificate_group is not None:
            self.ca_certificate_group = ca_certificate_group

    @property
    def name(self):
        """Gets the name of this SyslogServerSetting.  # noqa: E501

        The name of the object  # noqa: E501

        :return: The name of this SyslogServerSetting.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SyslogServerSetting.

        The name of the object  # noqa: E501

        :param name: The name of this SyslogServerSetting.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def id(self):
        """Gets the id of this SyslogServerSetting.  # noqa: E501

        A unique ID chosen by the system. Cannot change.  # noqa: E501

        :return: The id of this SyslogServerSetting.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this SyslogServerSetting.

        A unique ID chosen by the system. Cannot change.  # noqa: E501

        :param id: The id of this SyslogServerSetting.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def ca_certificate(self):
        """Gets the ca_certificate of this SyslogServerSetting.  # noqa: E501

        CA certificate used to validate the authenticity of the configured servers.  # noqa: E501

        :return: The ca_certificate of this SyslogServerSetting.  # noqa: E501
        :rtype: Reference
        """
        return self._ca_certificate

    @ca_certificate.setter
    def ca_certificate(self, ca_certificate):
        """Sets the ca_certificate of this SyslogServerSetting.

        CA certificate used to validate the authenticity of the configured servers.  # noqa: E501

        :param ca_certificate: The ca_certificate of this SyslogServerSetting.  # noqa: E501
        :type: Reference
        """

        self._ca_certificate = ca_certificate

    @property
    def ca_certificate_group(self):
        """Gets the ca_certificate_group of this SyslogServerSetting.  # noqa: E501

        A certificate group containing CA certificates that can be used to validate the authenticity of the configured servers.  # noqa: E501

        :return: The ca_certificate_group of this SyslogServerSetting.  # noqa: E501
        :rtype: Reference
        """
        return self._ca_certificate_group

    @ca_certificate_group.setter
    def ca_certificate_group(self, ca_certificate_group):
        """Sets the ca_certificate_group of this SyslogServerSetting.

        A certificate group containing CA certificates that can be used to validate the authenticity of the configured servers.  # noqa: E501

        :param ca_certificate_group: The ca_certificate_group of this SyslogServerSetting.  # noqa: E501
        :type: Reference
        """

        self._ca_certificate_group = ca_certificate_group

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
        if issubclass(SyslogServerSetting, dict):
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
        if not isinstance(other, SyslogServerSetting):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
