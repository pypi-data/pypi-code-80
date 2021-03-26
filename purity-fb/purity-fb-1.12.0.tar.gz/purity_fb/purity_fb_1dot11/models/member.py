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


class Member(object):
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
        'member': 'Reference',
        'group': 'Reference'
    }

    attribute_map = {
        'member': 'member',
        'group': 'group'
    }

    def __init__(self, member=None, group=None):  # noqa: E501
        """Member - a model defined in Swagger"""  # noqa: E501

        self._member = None
        self._group = None
        self.discriminator = None

        if member is not None:
            self.member = member
        if group is not None:
            self.group = group

    @property
    def member(self):
        """Gets the member of this Member.  # noqa: E501

        A reference to an object that is a member of the referenced group.  # noqa: E501

        :return: The member of this Member.  # noqa: E501
        :rtype: Reference
        """
        return self._member

    @member.setter
    def member(self, member):
        """Sets the member of this Member.

        A reference to an object that is a member of the referenced group.  # noqa: E501

        :param member: The member of this Member.  # noqa: E501
        :type: Reference
        """

        self._member = member

    @property
    def group(self):
        """Gets the group of this Member.  # noqa: E501

        A reference to a group object that has the referenced member object as a member.  # noqa: E501

        :return: The group of this Member.  # noqa: E501
        :rtype: Reference
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this Member.

        A reference to a group object that has the referenced member object as a member.  # noqa: E501

        :param group: The group of this Member.  # noqa: E501
        :type: Reference
        """

        self._group = group

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
        if issubclass(Member, dict):
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
        if not isinstance(other, Member):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
