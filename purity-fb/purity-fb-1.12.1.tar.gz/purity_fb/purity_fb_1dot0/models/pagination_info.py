# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.0 Python SDK

    Pure Storage FlashBlade REST 1.0 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.0
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PaginationInfo(object):
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
        'total_item_count': 'int',
        'continuation_token': 'str'
    }

    attribute_map = {
        'total_item_count': 'total_item_count',
        'continuation_token': 'continuation_token'
    }

    def __init__(self, total_item_count=None, continuation_token=None):  # noqa: E501
        """PaginationInfo - a model defined in Swagger"""  # noqa: E501

        self._total_item_count = None
        self._continuation_token = None
        self.discriminator = None

        if total_item_count is not None:
            self.total_item_count = total_item_count
        if continuation_token is not None:
            self.continuation_token = continuation_token

    @property
    def total_item_count(self):
        """Gets the total_item_count of this PaginationInfo.  # noqa: E501

        total number of items  # noqa: E501

        :return: The total_item_count of this PaginationInfo.  # noqa: E501
        :rtype: int
        """
        return self._total_item_count

    @total_item_count.setter
    def total_item_count(self, total_item_count):
        """Sets the total_item_count of this PaginationInfo.

        total number of items  # noqa: E501

        :param total_item_count: The total_item_count of this PaginationInfo.  # noqa: E501
        :type: int
        """

        self._total_item_count = total_item_count

    @property
    def continuation_token(self):
        """Gets the continuation_token of this PaginationInfo.  # noqa: E501

        continuation token  # noqa: E501

        :return: The continuation_token of this PaginationInfo.  # noqa: E501
        :rtype: str
        """
        return self._continuation_token

    @continuation_token.setter
    def continuation_token(self, continuation_token):
        """Sets the continuation_token of this PaginationInfo.

        continuation token  # noqa: E501

        :param continuation_token: The continuation_token of this PaginationInfo.  # noqa: E501
        :type: str
        """

        self._continuation_token = continuation_token

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
        if issubclass(PaginationInfo, dict):
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
        if not isinstance(other, PaginationInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
