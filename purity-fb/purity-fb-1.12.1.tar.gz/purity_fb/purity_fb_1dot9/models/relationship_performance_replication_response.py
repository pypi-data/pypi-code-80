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


class RelationshipPerformanceReplicationResponse(object):
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
        'pagination_info': 'PaginationInfo',
        'items': 'list[RelationshipPerformanceReplication]',
        'total': 'list[RelationshipPerformanceReplication]'
    }

    attribute_map = {
        'pagination_info': 'pagination_info',
        'items': 'items',
        'total': 'total'
    }

    def __init__(self, pagination_info=None, items=None, total=None):  # noqa: E501
        """RelationshipPerformanceReplicationResponse - a model defined in Swagger"""  # noqa: E501

        self._pagination_info = None
        self._items = None
        self._total = None
        self.discriminator = None

        if pagination_info is not None:
            self.pagination_info = pagination_info
        if items is not None:
            self.items = items
        if total is not None:
            self.total = total

    @property
    def pagination_info(self):
        """Gets the pagination_info of this RelationshipPerformanceReplicationResponse.  # noqa: E501

        pagination information, only available in GET requests  # noqa: E501

        :return: The pagination_info of this RelationshipPerformanceReplicationResponse.  # noqa: E501
        :rtype: PaginationInfo
        """
        return self._pagination_info

    @pagination_info.setter
    def pagination_info(self, pagination_info):
        """Sets the pagination_info of this RelationshipPerformanceReplicationResponse.

        pagination information, only available in GET requests  # noqa: E501

        :param pagination_info: The pagination_info of this RelationshipPerformanceReplicationResponse.  # noqa: E501
        :type: PaginationInfo
        """

        self._pagination_info = pagination_info

    @property
    def items(self):
        """Gets the items of this RelationshipPerformanceReplicationResponse.  # noqa: E501

        A list of replication performance objects.  # noqa: E501

        :return: The items of this RelationshipPerformanceReplicationResponse.  # noqa: E501
        :rtype: list[RelationshipPerformanceReplication]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this RelationshipPerformanceReplicationResponse.

        A list of replication performance objects.  # noqa: E501

        :param items: The items of this RelationshipPerformanceReplicationResponse.  # noqa: E501
        :type: list[RelationshipPerformanceReplication]
        """

        self._items = items

    @property
    def total(self):
        """Gets the total of this RelationshipPerformanceReplicationResponse.  # noqa: E501

        A replication performance object containing totaled values; only available in GET requests.  # noqa: E501

        :return: The total of this RelationshipPerformanceReplicationResponse.  # noqa: E501
        :rtype: list[RelationshipPerformanceReplication]
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this RelationshipPerformanceReplicationResponse.

        A replication performance object containing totaled values; only available in GET requests.  # noqa: E501

        :param total: The total of this RelationshipPerformanceReplicationResponse.  # noqa: E501
        :type: list[RelationshipPerformanceReplication]
        """

        self._total = total

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
        if issubclass(RelationshipPerformanceReplicationResponse, dict):
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
        if not isinstance(other, RelationshipPerformanceReplicationResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
