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
        'id': 'str',
        'destroyed': 'bool',
        'owner': 'Reference',
        'owner_destroyed': 'bool',
        'policy': 'LocationReference',
        'source': 'str',
        'source_destroyed': 'bool',
        'source_id': 'str',
        'source_is_local': 'bool',
        'source_location': 'Reference',
        'source_display_name': 'str',
        'suffix': 'str',
        'time_remaining': 'int'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'destroyed': 'destroyed',
        'owner': 'owner',
        'owner_destroyed': 'owner_destroyed',
        'policy': 'policy',
        'source': 'source',
        'source_destroyed': 'source_destroyed',
        'source_id': 'source_id',
        'source_is_local': 'source_is_local',
        'source_location': 'source_location',
        'source_display_name': 'source_display_name',
        'suffix': 'suffix',
        'time_remaining': 'time_remaining'
    }

    def __init__(self, name=None, id=None, destroyed=None, owner=None, owner_destroyed=None, policy=None, source=None, source_destroyed=None, source_id=None, source_is_local=None, source_location=None, source_display_name=None, suffix=None, time_remaining=None):  # noqa: E501
        """FileSystemSnapshot - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._id = None
        self._destroyed = None
        self._owner = None
        self._owner_destroyed = None
        self._policy = None
        self._source = None
        self._source_destroyed = None
        self._source_id = None
        self._source_is_local = None
        self._source_location = None
        self._source_display_name = None
        self._suffix = None
        self._time_remaining = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if id is not None:
            self.id = id
        if destroyed is not None:
            self.destroyed = destroyed
        if owner is not None:
            self.owner = owner
        if owner_destroyed is not None:
            self.owner_destroyed = owner_destroyed
        if policy is not None:
            self.policy = policy
        if source is not None:
            self.source = source
        if source_destroyed is not None:
            self.source_destroyed = source_destroyed
        if source_id is not None:
            self.source_id = source_id
        if source_is_local is not None:
            self.source_is_local = source_is_local
        if source_location is not None:
            self.source_location = source_location
        if source_display_name is not None:
            self.source_display_name = source_display_name
        if suffix is not None:
            self.suffix = suffix
        if time_remaining is not None:
            self.time_remaining = time_remaining

    @property
    def name(self):
        """Gets the name of this FileSystemSnapshot.  # noqa: E501

        The name of the object  # noqa: E501

        :return: The name of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this FileSystemSnapshot.

        The name of the object  # noqa: E501

        :param name: The name of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def id(self):
        """Gets the id of this FileSystemSnapshot.  # noqa: E501

        A unique ID chosen by the system. Cannot change.  # noqa: E501

        :return: The id of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this FileSystemSnapshot.

        A unique ID chosen by the system. Cannot change.  # noqa: E501

        :param id: The id of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def destroyed(self):
        """Gets the destroyed of this FileSystemSnapshot.  # noqa: E501

        Is the file system snapshot destroyed? False by default.  # noqa: E501

        :return: The destroyed of this FileSystemSnapshot.  # noqa: E501
        :rtype: bool
        """
        return self._destroyed

    @destroyed.setter
    def destroyed(self, destroyed):
        """Sets the destroyed of this FileSystemSnapshot.

        Is the file system snapshot destroyed? False by default.  # noqa: E501

        :param destroyed: The destroyed of this FileSystemSnapshot.  # noqa: E501
        :type: bool
        """

        self._destroyed = destroyed

    @property
    def owner(self):
        """Gets the owner of this FileSystemSnapshot.  # noqa: E501

        A reference to the file system that owns this snapshot. If the owner is destroyed, this will be destroyed.  # noqa: E501

        :return: The owner of this FileSystemSnapshot.  # noqa: E501
        :rtype: Reference
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this FileSystemSnapshot.

        A reference to the file system that owns this snapshot. If the owner is destroyed, this will be destroyed.  # noqa: E501

        :param owner: The owner of this FileSystemSnapshot.  # noqa: E501
        :type: Reference
        """

        self._owner = owner

    @property
    def owner_destroyed(self):
        """Gets the owner_destroyed of this FileSystemSnapshot.  # noqa: E501

        Is the owning file system destroyed?  # noqa: E501

        :return: The owner_destroyed of this FileSystemSnapshot.  # noqa: E501
        :rtype: bool
        """
        return self._owner_destroyed

    @owner_destroyed.setter
    def owner_destroyed(self, owner_destroyed):
        """Sets the owner_destroyed of this FileSystemSnapshot.

        Is the owning file system destroyed?  # noqa: E501

        :param owner_destroyed: The owner_destroyed of this FileSystemSnapshot.  # noqa: E501
        :type: bool
        """

        self._owner_destroyed = owner_destroyed

    @property
    def policy(self):
        """Gets the policy of this FileSystemSnapshot.  # noqa: E501

        A reference to the associated policy.  # noqa: E501

        :return: The policy of this FileSystemSnapshot.  # noqa: E501
        :rtype: LocationReference
        """
        return self._policy

    @policy.setter
    def policy(self, policy):
        """Sets the policy of this FileSystemSnapshot.

        A reference to the associated policy.  # noqa: E501

        :param policy: The policy of this FileSystemSnapshot.  # noqa: E501
        :type: LocationReference
        """

        self._policy = policy

    @property
    def source(self):
        """Gets the source of this FileSystemSnapshot.  # noqa: E501

        The name of the file system that was the source of the data in this snapshot. Normally this is the same as the owner, but if the snapshot is replicated, the source is the original file system.  # noqa: E501

        :return: The source of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this FileSystemSnapshot.

        The name of the file system that was the source of the data in this snapshot. Normally this is the same as the owner, but if the snapshot is replicated, the source is the original file system.  # noqa: E501

        :param source: The source of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def source_destroyed(self):
        """Gets the source_destroyed of this FileSystemSnapshot.  # noqa: E501

        Deprecated. Use `owner_destroyed`. Is the owning file system destroyed?  # noqa: E501

        :return: The source_destroyed of this FileSystemSnapshot.  # noqa: E501
        :rtype: bool
        """
        return self._source_destroyed

    @source_destroyed.setter
    def source_destroyed(self, source_destroyed):
        """Sets the source_destroyed of this FileSystemSnapshot.

        Deprecated. Use `owner_destroyed`. Is the owning file system destroyed?  # noqa: E501

        :param source_destroyed: The source_destroyed of this FileSystemSnapshot.  # noqa: E501
        :type: bool
        """

        self._source_destroyed = source_destroyed

    @property
    def source_id(self):
        """Gets the source_id of this FileSystemSnapshot.  # noqa: E501

        The unique global ID of the source file system.  # noqa: E501

        :return: The source_id of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        """Sets the source_id of this FileSystemSnapshot.

        The unique global ID of the source file system.  # noqa: E501

        :param source_id: The source_id of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._source_id = source_id

    @property
    def source_is_local(self):
        """Gets the source_is_local of this FileSystemSnapshot.  # noqa: E501

        Is the source of this file system snapshot on the local array?  # noqa: E501

        :return: The source_is_local of this FileSystemSnapshot.  # noqa: E501
        :rtype: bool
        """
        return self._source_is_local

    @source_is_local.setter
    def source_is_local(self, source_is_local):
        """Sets the source_is_local of this FileSystemSnapshot.

        Is the source of this file system snapshot on the local array?  # noqa: E501

        :param source_is_local: The source_is_local of this FileSystemSnapshot.  # noqa: E501
        :type: bool
        """

        self._source_is_local = source_is_local

    @property
    def source_location(self):
        """Gets the source_location of this FileSystemSnapshot.  # noqa: E501

        A reference to the source array.  # noqa: E501

        :return: The source_location of this FileSystemSnapshot.  # noqa: E501
        :rtype: Reference
        """
        return self._source_location

    @source_location.setter
    def source_location(self, source_location):
        """Sets the source_location of this FileSystemSnapshot.

        A reference to the source array.  # noqa: E501

        :param source_location: The source_location of this FileSystemSnapshot.  # noqa: E501
        :type: Reference
        """

        self._source_location = source_location

    @property
    def source_display_name(self):
        """Gets the source_display_name of this FileSystemSnapshot.  # noqa: E501

        Full name of the source with remote array information. Response will be same as source for local file system snapshots.  # noqa: E501

        :return: The source_display_name of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._source_display_name

    @source_display_name.setter
    def source_display_name(self, source_display_name):
        """Sets the source_display_name of this FileSystemSnapshot.

        Full name of the source with remote array information. Response will be same as source for local file system snapshots.  # noqa: E501

        :param source_display_name: The source_display_name of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._source_display_name = source_display_name

    @property
    def suffix(self):
        """Gets the suffix of this FileSystemSnapshot.  # noqa: E501

        The suffix of the snapshot, e.g., snap1.  # noqa: E501

        :return: The suffix of this FileSystemSnapshot.  # noqa: E501
        :rtype: str
        """
        return self._suffix

    @suffix.setter
    def suffix(self, suffix):
        """Sets the suffix of this FileSystemSnapshot.

        The suffix of the snapshot, e.g., snap1.  # noqa: E501

        :param suffix: The suffix of this FileSystemSnapshot.  # noqa: E501
        :type: str
        """

        self._suffix = suffix

    @property
    def time_remaining(self):
        """Gets the time_remaining of this FileSystemSnapshot.  # noqa: E501

        Time in milliseconds before the file system snapshot is eradicated. Null if not destroyed.  # noqa: E501

        :return: The time_remaining of this FileSystemSnapshot.  # noqa: E501
        :rtype: int
        """
        return self._time_remaining

    @time_remaining.setter
    def time_remaining(self, time_remaining):
        """Sets the time_remaining of this FileSystemSnapshot.

        Time in milliseconds before the file system snapshot is eradicated. Null if not destroyed.  # noqa: E501

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
