# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.9 Python SDK

    Pure Storage FlashBlade REST 1.9 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.9
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class MemberLink(object):
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
        'local_file_system': 'FixedReferenceWithId',
        'remote': 'FixedReferenceWithId',
        'remote_file_system': 'FixedReferenceNoResourceType'
    }

    attribute_map = {
        'local_file_system': 'local_file_system',
        'remote': 'remote',
        'remote_file_system': 'remote_file_system'
    }

    def __init__(self, local_file_system=None, remote=None, remote_file_system=None):  # noqa: E501
        """MemberLink - a model defined in Swagger"""  # noqa: E501

        self._local_file_system = None
        self._remote = None
        self._remote_file_system = None
        self.discriminator = None

        if local_file_system is not None:
            self.local_file_system = local_file_system
        if remote is not None:
            self.remote = remote
        if remote_file_system is not None:
            self.remote_file_system = remote_file_system

    @property
    def local_file_system(self):
        """Gets the local_file_system of this MemberLink.  # noqa: E501


        :return: The local_file_system of this MemberLink.  # noqa: E501
        :rtype: FixedReferenceWithId
        """
        return self._local_file_system

    @local_file_system.setter
    def local_file_system(self, local_file_system):
        """Sets the local_file_system of this MemberLink.


        :param local_file_system: The local_file_system of this MemberLink.  # noqa: E501
        :type: FixedReferenceWithId
        """

        self._local_file_system = local_file_system

    @property
    def remote(self):
        """Gets the remote of this MemberLink.  # noqa: E501


        :return: The remote of this MemberLink.  # noqa: E501
        :rtype: FixedReferenceWithId
        """
        return self._remote

    @remote.setter
    def remote(self, remote):
        """Sets the remote of this MemberLink.


        :param remote: The remote of this MemberLink.  # noqa: E501
        :type: FixedReferenceWithId
        """

        self._remote = remote

    @property
    def remote_file_system(self):
        """Gets the remote_file_system of this MemberLink.  # noqa: E501


        :return: The remote_file_system of this MemberLink.  # noqa: E501
        :rtype: FixedReferenceNoResourceType
        """
        return self._remote_file_system

    @remote_file_system.setter
    def remote_file_system(self, remote_file_system):
        """Sets the remote_file_system of this MemberLink.


        :param remote_file_system: The remote_file_system of this MemberLink.  # noqa: E501
        :type: FixedReferenceNoResourceType
        """

        self._remote_file_system = remote_file_system

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
        if issubclass(MemberLink, dict):
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
        if not isinstance(other, MemberLink):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
