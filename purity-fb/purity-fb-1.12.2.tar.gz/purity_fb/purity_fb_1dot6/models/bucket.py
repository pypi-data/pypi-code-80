# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.6 Python SDK

    Pure Storage FlashBlade REST 1.6 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.6
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Bucket(object):
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
        'space': 'Space',
        'account': 'Reference',
        'destroyed': 'bool',
        'time_remaining': 'int',
        'object_count': 'int',
        'versioning': 'str'
    }

    attribute_map = {
        'name': 'name',
        'created': 'created',
        'space': 'space',
        'account': 'account',
        'destroyed': 'destroyed',
        'time_remaining': 'time_remaining',
        'object_count': 'object_count',
        'versioning': 'versioning'
    }

    def __init__(self, name=None, created=None, space=None, account=None, destroyed=None, time_remaining=None, object_count=None, versioning=None):  # noqa: E501
        """Bucket - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._created = None
        self._space = None
        self._account = None
        self._destroyed = None
        self._time_remaining = None
        self._object_count = None
        self._versioning = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if created is not None:
            self.created = created
        if space is not None:
            self.space = space
        if account is not None:
            self.account = account
        if destroyed is not None:
            self.destroyed = destroyed
        if time_remaining is not None:
            self.time_remaining = time_remaining
        if object_count is not None:
            self.object_count = object_count
        if versioning is not None:
            self.versioning = versioning

    @property
    def name(self):
        """Gets the name of this Bucket.  # noqa: E501

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :return: The name of this Bucket.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Bucket.

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :param name: The name of this Bucket.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def created(self):
        """Gets the created of this Bucket.  # noqa: E501

        Creation timestamp of the object  # noqa: E501

        :return: The created of this Bucket.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Bucket.

        Creation timestamp of the object  # noqa: E501

        :param created: The created of this Bucket.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def space(self):
        """Gets the space of this Bucket.  # noqa: E501

        the space specification of the bucket  # noqa: E501

        :return: The space of this Bucket.  # noqa: E501
        :rtype: Space
        """
        return self._space

    @space.setter
    def space(self, space):
        """Sets the space of this Bucket.

        the space specification of the bucket  # noqa: E501

        :param space: The space of this Bucket.  # noqa: E501
        :type: Space
        """

        self._space = space

    @property
    def account(self):
        """Gets the account of this Bucket.  # noqa: E501

        the account of the bucket  # noqa: E501

        :return: The account of this Bucket.  # noqa: E501
        :rtype: Reference
        """
        return self._account

    @account.setter
    def account(self, account):
        """Sets the account of this Bucket.

        the account of the bucket  # noqa: E501

        :param account: The account of this Bucket.  # noqa: E501
        :type: Reference
        """

        self._account = account

    @property
    def destroyed(self):
        """Gets the destroyed of this Bucket.  # noqa: E501

        is the bucket destroyed? False by default. Modifiable.  # noqa: E501

        :return: The destroyed of this Bucket.  # noqa: E501
        :rtype: bool
        """
        return self._destroyed

    @destroyed.setter
    def destroyed(self, destroyed):
        """Sets the destroyed of this Bucket.

        is the bucket destroyed? False by default. Modifiable.  # noqa: E501

        :param destroyed: The destroyed of this Bucket.  # noqa: E501
        :type: bool
        """

        self._destroyed = destroyed

    @property
    def time_remaining(self):
        """Gets the time_remaining of this Bucket.  # noqa: E501

        time in milliseconds before the bucket is eradicated. Null if not destroyed.  # noqa: E501

        :return: The time_remaining of this Bucket.  # noqa: E501
        :rtype: int
        """
        return self._time_remaining

    @time_remaining.setter
    def time_remaining(self, time_remaining):
        """Sets the time_remaining of this Bucket.

        time in milliseconds before the bucket is eradicated. Null if not destroyed.  # noqa: E501

        :param time_remaining: The time_remaining of this Bucket.  # noqa: E501
        :type: int
        """

        self._time_remaining = time_remaining

    @property
    def object_count(self):
        """Gets the object_count of this Bucket.  # noqa: E501

        the number of object within the bucket.  # noqa: E501

        :return: The object_count of this Bucket.  # noqa: E501
        :rtype: int
        """
        return self._object_count

    @object_count.setter
    def object_count(self, object_count):
        """Sets the object_count of this Bucket.

        the number of object within the bucket.  # noqa: E501

        :param object_count: The object_count of this Bucket.  # noqa: E501
        :type: int
        """

        self._object_count = object_count

    @property
    def versioning(self):
        """Gets the versioning of this Bucket.  # noqa: E501

        the versioning state for objects within the bucket. Possible values are none, enabled, and suspended.  # noqa: E501

        :return: The versioning of this Bucket.  # noqa: E501
        :rtype: str
        """
        return self._versioning

    @versioning.setter
    def versioning(self, versioning):
        """Sets the versioning of this Bucket.

        the versioning state for objects within the bucket. Possible values are none, enabled, and suspended.  # noqa: E501

        :param versioning: The versioning of this Bucket.  # noqa: E501
        :type: str
        """

        self._versioning = versioning

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
        if issubclass(Bucket, dict):
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
        if not isinstance(other, Bucket):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
