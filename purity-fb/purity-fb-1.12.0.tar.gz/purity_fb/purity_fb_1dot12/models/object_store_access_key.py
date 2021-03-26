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


class ObjectStoreAccessKey(object):
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
        'created': 'int',
        'user': 'Reference',
        'enabled': 'bool',
        'secret_access_key': 'str'
    }

    attribute_map = {
        'name': 'name',
        'created': 'created',
        'user': 'user',
        'enabled': 'enabled',
        'secret_access_key': 'secret_access_key'
    }

    def __init__(self, name=None, created=None, user=None, enabled=None, secret_access_key=None):  # noqa: E501
        """ObjectStoreAccessKey - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._created = None
        self._user = None
        self._enabled = None
        self._secret_access_key = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if created is not None:
            self.created = created
        if user is not None:
            self.user = user
        if enabled is not None:
            self.enabled = enabled
        if secret_access_key is not None:
            self.secret_access_key = secret_access_key

    @property
    def name(self):
        """Gets the name of this ObjectStoreAccessKey.  # noqa: E501

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :return: The name of this ObjectStoreAccessKey.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ObjectStoreAccessKey.

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :param name: The name of this ObjectStoreAccessKey.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def created(self):
        """Gets the created of this ObjectStoreAccessKey.  # noqa: E501

        Creation timestamp of the object  # noqa: E501

        :return: The created of this ObjectStoreAccessKey.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this ObjectStoreAccessKey.

        Creation timestamp of the object  # noqa: E501

        :param created: The created of this ObjectStoreAccessKey.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def user(self):
        """Gets the user of this ObjectStoreAccessKey.  # noqa: E501

        Reference to the associated user.  # noqa: E501

        :return: The user of this ObjectStoreAccessKey.  # noqa: E501
        :rtype: Reference
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this ObjectStoreAccessKey.

        Reference to the associated user.  # noqa: E501

        :param user: The user of this ObjectStoreAccessKey.  # noqa: E501
        :type: Reference
        """

        self._user = user

    @property
    def enabled(self):
        """Gets the enabled of this ObjectStoreAccessKey.  # noqa: E501

        Is the access key enabled? Default is true.  # noqa: E501

        :return: The enabled of this ObjectStoreAccessKey.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this ObjectStoreAccessKey.

        Is the access key enabled? Default is true.  # noqa: E501

        :param enabled: The enabled of this ObjectStoreAccessKey.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def secret_access_key(self):
        """Gets the secret_access_key of this ObjectStoreAccessKey.  # noqa: E501

        The secret access key, only populated on creation if it is not imported from another FlashBlade.  # noqa: E501

        :return: The secret_access_key of this ObjectStoreAccessKey.  # noqa: E501
        :rtype: str
        """
        return self._secret_access_key

    @secret_access_key.setter
    def secret_access_key(self, secret_access_key):
        """Sets the secret_access_key of this ObjectStoreAccessKey.

        The secret access key, only populated on creation if it is not imported from another FlashBlade.  # noqa: E501

        :param secret_access_key: The secret_access_key of this ObjectStoreAccessKey.  # noqa: E501
        :type: str
        """

        self._secret_access_key = secret_access_key

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
        if issubclass(ObjectStoreAccessKey, dict):
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
        if not isinstance(other, ObjectStoreAccessKey):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
