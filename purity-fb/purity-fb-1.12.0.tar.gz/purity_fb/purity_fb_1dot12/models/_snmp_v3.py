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


class SnmpV3(object):
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
        'auth_passphrase': 'str',
        'auth_protocol': 'str',
        'privacy_passphrase': 'str',
        'privacy_protocol': 'str',
        'user': 'str'
    }

    attribute_map = {
        'auth_passphrase': 'auth_passphrase',
        'auth_protocol': 'auth_protocol',
        'privacy_passphrase': 'privacy_passphrase',
        'privacy_protocol': 'privacy_protocol',
        'user': 'user'
    }

    def __init__(self, auth_passphrase=None, auth_protocol=None, privacy_passphrase=None, privacy_protocol=None, user=None):  # noqa: E501
        """SnmpV3 - a model defined in Swagger"""  # noqa: E501

        self._auth_passphrase = None
        self._auth_protocol = None
        self._privacy_passphrase = None
        self._privacy_protocol = None
        self._user = None
        self.discriminator = None

        if auth_passphrase is not None:
            self.auth_passphrase = auth_passphrase
        if auth_protocol is not None:
            self.auth_protocol = auth_protocol
        if privacy_passphrase is not None:
            self.privacy_passphrase = privacy_passphrase
        if privacy_protocol is not None:
            self.privacy_protocol = privacy_protocol
        if user is not None:
            self.user = user

    @property
    def auth_passphrase(self):
        """Gets the auth_passphrase of this SnmpV3.  # noqa: E501

        Passphrase used by Purity to authenticate the array with the specified managers.  # noqa: E501

        :return: The auth_passphrase of this SnmpV3.  # noqa: E501
        :rtype: str
        """
        return self._auth_passphrase

    @auth_passphrase.setter
    def auth_passphrase(self, auth_passphrase):
        """Sets the auth_passphrase of this SnmpV3.

        Passphrase used by Purity to authenticate the array with the specified managers.  # noqa: E501

        :param auth_passphrase: The auth_passphrase of this SnmpV3.  # noqa: E501
        :type: str
        """
        if auth_passphrase is not None and len(auth_passphrase) > 32:
            raise ValueError("Invalid value for `auth_passphrase`, length must be less than or equal to `32`")  # noqa: E501

        self._auth_passphrase = auth_passphrase

    @property
    def auth_protocol(self):
        """Gets the auth_protocol of this SnmpV3.  # noqa: E501

        Hash algorithm used to validate the authentication passphrase. Valid values are `MD5` and `SHA`.  # noqa: E501

        :return: The auth_protocol of this SnmpV3.  # noqa: E501
        :rtype: str
        """
        return self._auth_protocol

    @auth_protocol.setter
    def auth_protocol(self, auth_protocol):
        """Sets the auth_protocol of this SnmpV3.

        Hash algorithm used to validate the authentication passphrase. Valid values are `MD5` and `SHA`.  # noqa: E501

        :param auth_protocol: The auth_protocol of this SnmpV3.  # noqa: E501
        :type: str
        """

        self._auth_protocol = auth_protocol

    @property
    def privacy_passphrase(self):
        """Gets the privacy_passphrase of this SnmpV3.  # noqa: E501

        Passphrase used to encrypt SNMP messages. A passphrase must be at least 8 characters in length, and may be at most 63 characters in length.  # noqa: E501

        :return: The privacy_passphrase of this SnmpV3.  # noqa: E501
        :rtype: str
        """
        return self._privacy_passphrase

    @privacy_passphrase.setter
    def privacy_passphrase(self, privacy_passphrase):
        """Sets the privacy_passphrase of this SnmpV3.

        Passphrase used to encrypt SNMP messages. A passphrase must be at least 8 characters in length, and may be at most 63 characters in length.  # noqa: E501

        :param privacy_passphrase: The privacy_passphrase of this SnmpV3.  # noqa: E501
        :type: str
        """

        self._privacy_passphrase = privacy_passphrase

    @property
    def privacy_protocol(self):
        """Gets the privacy_protocol of this SnmpV3.  # noqa: E501

        Encryption protocol for SNMP messages. Valid values are `AES` and `DES`.  # noqa: E501

        :return: The privacy_protocol of this SnmpV3.  # noqa: E501
        :rtype: str
        """
        return self._privacy_protocol

    @privacy_protocol.setter
    def privacy_protocol(self, privacy_protocol):
        """Sets the privacy_protocol of this SnmpV3.

        Encryption protocol for SNMP messages. Valid values are `AES` and `DES`.  # noqa: E501

        :param privacy_protocol: The privacy_protocol of this SnmpV3.  # noqa: E501
        :type: str
        """

        self._privacy_protocol = privacy_protocol

    @property
    def user(self):
        """Gets the user of this SnmpV3.  # noqa: E501

        User ID recognized by the specified SNMP managers which Purity is to use in communications with them.  # noqa: E501

        :return: The user of this SnmpV3.  # noqa: E501
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this SnmpV3.

        User ID recognized by the specified SNMP managers which Purity is to use in communications with them.  # noqa: E501

        :param user: The user of this SnmpV3.  # noqa: E501
        :type: str
        """

        self._user = user

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
        if issubclass(SnmpV3, dict):
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
        if not isinstance(other, SnmpV3):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
