# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.10 Python SDK

    Pure Storage FlashBlade REST 1.10 Python SDK. Compatible with REST API versions 1.0 - 1.10. Developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.10
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class DirectoryserviceManagement(object):
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
        'user_login_attribute': 'str',
        'user_object_class': 'str'
    }

    attribute_map = {
        'user_login_attribute': 'user_login_attribute',
        'user_object_class': 'user_object_class'
    }

    def __init__(self, user_login_attribute=None, user_object_class=None):  # noqa: E501
        """DirectoryserviceManagement - a model defined in Swagger"""  # noqa: E501

        self._user_login_attribute = None
        self._user_object_class = None
        self.discriminator = None

        if user_login_attribute is not None:
            self.user_login_attribute = user_login_attribute
        if user_object_class is not None:
            self.user_object_class = user_object_class

    @property
    def user_login_attribute(self):
        """Gets the user_login_attribute of this DirectoryserviceManagement.  # noqa: E501

        User login attribute in the structure of the configured LDAP servers. Typically the attribute field that holds the user’s unique login name. Defaults to `sAMAccountName` for Active Directory servers, or `uid` for all other directory server types.   # noqa: E501

        :return: The user_login_attribute of this DirectoryserviceManagement.  # noqa: E501
        :rtype: str
        """
        return self._user_login_attribute

    @user_login_attribute.setter
    def user_login_attribute(self, user_login_attribute):
        """Sets the user_login_attribute of this DirectoryserviceManagement.

        User login attribute in the structure of the configured LDAP servers. Typically the attribute field that holds the user’s unique login name. Defaults to `sAMAccountName` for Active Directory servers, or `uid` for all other directory server types.   # noqa: E501

        :param user_login_attribute: The user_login_attribute of this DirectoryserviceManagement.  # noqa: E501
        :type: str
        """

        self._user_login_attribute = user_login_attribute

    @property
    def user_object_class(self):
        """Gets the user_object_class of this DirectoryserviceManagement.  # noqa: E501

        Value of the object class for a management LDAP user. Defaults to `User` for Active Directory servers, `posixAccount` or `shadowAccount` for OpenLDAP servers dependent on the server's group type, or `person` for all other directory servers.   # noqa: E501

        :return: The user_object_class of this DirectoryserviceManagement.  # noqa: E501
        :rtype: str
        """
        return self._user_object_class

    @user_object_class.setter
    def user_object_class(self, user_object_class):
        """Sets the user_object_class of this DirectoryserviceManagement.

        Value of the object class for a management LDAP user. Defaults to `User` for Active Directory servers, `posixAccount` or `shadowAccount` for OpenLDAP servers dependent on the server's group type, or `person` for all other directory servers.   # noqa: E501

        :param user_object_class: The user_object_class of this DirectoryserviceManagement.  # noqa: E501
        :type: str
        """

        self._user_object_class = user_object_class

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
        if issubclass(DirectoryserviceManagement, dict):
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
        if not isinstance(other, DirectoryserviceManagement):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
