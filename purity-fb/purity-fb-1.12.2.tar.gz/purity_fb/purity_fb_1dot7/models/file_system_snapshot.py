# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.7 Python SDK

    Pure Storage FlashBlade REST 1.7 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.7
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class FileSystemSnapshot(object):
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
        'suffix': 'str',
        'source': 'str',
        'destroyed': 'bool',
        'source_destroyed': 'bool',
        'time_remaining': 'int'
    }

    attribute_map = {
        'name': 'name',
        'created': 'created',
        'suffix': 'suffix',
        'source': 'source',
        'destroyed': 'destroyed',
        'source_destroyed': 'source_destroyed',
        'time_remaining': 'time_remaining'
    }

    def __init__(self, name=None, created=None, suffix=None, source=None, destroyed=None, source_destroyed=None, time_remaining=None):  # noqa: E501
        """FileSystemSnapshot - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._created = None
        self._suffix = None
        self._source = None
        self._destroyed = None
        self._source_destroyed = None
        self._time_remaining = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if created is not None:
            self.created = created
        if suffix is not None:
            self.suffix = suffix
        if source is not None:
            self.source = source
        if destroyed is not None:
            self.destroyed = destroyed
        if source_destroyed is not None:
            self.source_destroyed = source_destroyed
        if time_remaining is not None:
            self.time_remaining = time_remaining

    @property
    def name(self):
        """Gets the name of this FileSystemSnapshot.  # noqa: E501

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :return: The name of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FileSystemSnapshot.

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :param name: The name of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def created(self):
        """Gets the created of this FileSystemSnapshot.  # noqa: E501

        creation timestamp of the object  # noqa: E501

        :return: The created of this FileSystemSnapshot.  # noqa: E501
        :rtype: int
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this FileSystemSnapshot.

        creation timestamp of the object  # noqa: E501

        :param created: The created of this FileSystemSnapshot.  # noqa: E501
        :type: int
        """

        self._created = created

    @property
    def suffix(self):
        """Gets the suffix of this FileSystemSnapshot.  # noqa: E501

        the suffix of the snapshot, e.g., snap1  # noqa: E501

        :return: The suffix of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._suffix

    @suffix.setter
    def suffix(self, suffix):
        """Sets the suffix of this FileSystemSnapshot.

        the suffix of the snapshot, e.g., snap1  # noqa: E501

        :param suffix: The suffix of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._suffix = suffix

    @property
    def source(self):
        """Gets the source of this FileSystemSnapshot.  # noqa: E501

        the name of the source file system  # noqa: E501

        :return: The source of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this FileSystemSnapshot.

        the name of the source file system  # noqa: E501

        :param source: The source of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def destroyed(self):
        """Gets the destroyed of this FileSystemSnapshot.  # noqa: E501

        is the file system snapshot destroyed? False by default.  # noqa: E501

        :return: The destroyed of this FileSystemSnapshot.  # noqa: E501
        :rtype: bool
        """
        return self._destroyed

    @destroyed.setter
    def destroyed(self, destroyed):
        """Sets the destroyed of this FileSystemSnapshot.

        is the file system snapshot destroyed? False by default.  # noqa: E501

        :param destroyed: The destroyed of this FileSystemSnapshot.  # noqa: E501
        :type: bool
        """

        self._destroyed = destroyed

    @property
    def source_destroyed(self):
        """Gets the source_destroyed of this FileSystemSnapshot.  # noqa: E501

        is the source file system destroyed?  # noqa: E501

        :return: The source_destroyed of this FileSystemSnapshot.  # noqa: E501
        :rtype: bool
        """
        return self._source_destroyed

    @source_destroyed.setter
    def source_destroyed(self, source_destroyed):
        """Sets the source_destroyed of this FileSystemSnapshot.

        is the source file system destroyed?  # noqa: E501

        :param source_destroyed: The source_destroyed of this FileSystemSnapshot.  # noqa: E501
        :type: bool
        """

        self._source_destroyed = source_destroyed

    @property
    def time_remaining(self):
        """Gets the time_remaining of this FileSystemSnapshot.  # noqa: E501

        time in milliseconds before the file system snapshot is eradicated. Null if not destroyed.  # noqa: E501

        :return: The time_remaining of this FileSystemSnapshot.  # noqa: E501
        :rtype: int
        """
        return self._time_remaining

    @time_remaining.setter
    def time_remaining(self, time_remaining):
        """Sets the time_remaining of this FileSystemSnapshot.

        time in milliseconds before the file system snapshot is eradicated. Null if not destroyed.  # noqa: E501

        :param time_remaining: The time_remaining of this FileSystemSnapshot.  # noqa: E501
        :type: int
        """

        self._time_remaining = time_remaining

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
        if issubclass(FileSystemSnapshot, dict):
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
        if not isinstance(other, FileSystemSnapshot):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
