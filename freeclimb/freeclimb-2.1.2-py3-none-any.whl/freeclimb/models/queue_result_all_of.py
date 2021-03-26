# coding: utf-8

"""
    FreeClimb API

    FreeClimb is a cloud-based application programming interface (API) that puts the power of the Vail platform in your hands. FreeClimb simplifies the process of creating applications that can use a full range of telephony features without requiring specialized or on-site telephony equipment. Using the FreeClimb REST API to write applications is easy! You have the option to use the language of your choice or hit the API directly. Your application can execute a command by issuing a RESTful request to the FreeClimb API. The base URL to send HTTP requests to the FreeClimb REST API is: /apiserver. FreeClimb authenticates and processes your request.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Contact: support@freeclimb.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from freeclimb.configuration import Configuration


class QueueResultAllOf(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'account_id': 'str',
        'queue_id': 'str',
        'alias': 'str',
        'max_size': 'int',
        'current_size': 'str',
        'average_wait_time': 'str',
        'subresource_uris': 'object'
    }

    attribute_map = {
        'account_id': 'accountId',
        'queue_id': 'queueId',
        'alias': 'alias',
        'max_size': 'maxSize',
        'current_size': 'currentSize',
        'average_wait_time': 'averageWaitTime',
        'subresource_uris': 'subresourceUris'
    }

    def __init__(self, account_id=None, queue_id=None, alias=None, max_size=None, current_size=None, average_wait_time=None, subresource_uris=None, local_vars_configuration=None):  # noqa: E501
        """QueueResultAllOf - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._account_id = None
        self._queue_id = None
        self._alias = None
        self._max_size = None
        self._current_size = None
        self._average_wait_time = None
        self._subresource_uris = None
        self.discriminator = None

        if account_id is not None:
            self.account_id = account_id
        if queue_id is not None:
            self.queue_id = queue_id
        if alias is not None:
            self.alias = alias
        if max_size is not None:
            self.max_size = max_size
        if current_size is not None:
            self.current_size = current_size
        if average_wait_time is not None:
            self.average_wait_time = average_wait_time
        if subresource_uris is not None:
            self.subresource_uris = subresource_uris

    @property
    def account_id(self):
        """Gets the account_id of this QueueResultAllOf.  # noqa: E501

        ID of the account that created this Queue.  # noqa: E501

        :return: The account_id of this QueueResultAllOf.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this QueueResultAllOf.

        ID of the account that created this Queue.  # noqa: E501

        :param account_id: The account_id of this QueueResultAllOf.  # noqa: E501
        :type: str
        """

        self._account_id = account_id

    @property
    def queue_id(self):
        """Gets the queue_id of this QueueResultAllOf.  # noqa: E501

        A string that uniquely identifies this Queue resource.  # noqa: E501

        :return: The queue_id of this QueueResultAllOf.  # noqa: E501
        :rtype: str
        """
        return self._queue_id

    @queue_id.setter
    def queue_id(self, queue_id):
        """Sets the queue_id of this QueueResultAllOf.

        A string that uniquely identifies this Queue resource.  # noqa: E501

        :param queue_id: The queue_id of this QueueResultAllOf.  # noqa: E501
        :type: str
        """

        self._queue_id = queue_id

    @property
    def alias(self):
        """Gets the alias of this QueueResultAllOf.  # noqa: E501

        A description for this Queue.  # noqa: E501

        :return: The alias of this QueueResultAllOf.  # noqa: E501
        :rtype: str
        """
        return self._alias

    @alias.setter
    def alias(self, alias):
        """Sets the alias of this QueueResultAllOf.

        A description for this Queue.  # noqa: E501

        :param alias: The alias of this QueueResultAllOf.  # noqa: E501
        :type: str
        """

        self._alias = alias

    @property
    def max_size(self):
        """Gets the max_size of this QueueResultAllOf.  # noqa: E501

        The maximum number of Calls permitted in the Queue. Default is 100. Maximum is 1000.  # noqa: E501

        :return: The max_size of this QueueResultAllOf.  # noqa: E501
        :rtype: int
        """
        return self._max_size

    @max_size.setter
    def max_size(self, max_size):
        """Sets the max_size of this QueueResultAllOf.

        The maximum number of Calls permitted in the Queue. Default is 100. Maximum is 1000.  # noqa: E501

        :param max_size: The max_size of this QueueResultAllOf.  # noqa: E501
        :type: int
        """

        self._max_size = max_size

    @property
    def current_size(self):
        """Gets the current_size of this QueueResultAllOf.  # noqa: E501

        Count of Calls currently in the Queue.  # noqa: E501

        :return: The current_size of this QueueResultAllOf.  # noqa: E501
        :rtype: str
        """
        return self._current_size

    @current_size.setter
    def current_size(self, current_size):
        """Sets the current_size of this QueueResultAllOf.

        Count of Calls currently in the Queue.  # noqa: E501

        :param current_size: The current_size of this QueueResultAllOf.  # noqa: E501
        :type: str
        """

        self._current_size = current_size

    @property
    def average_wait_time(self):
        """Gets the average_wait_time of this QueueResultAllOf.  # noqa: E501

        Average wait time (in seconds) of all Calls in the Queue.  # noqa: E501

        :return: The average_wait_time of this QueueResultAllOf.  # noqa: E501
        :rtype: str
        """
        return self._average_wait_time

    @average_wait_time.setter
    def average_wait_time(self, average_wait_time):
        """Sets the average_wait_time of this QueueResultAllOf.

        Average wait time (in seconds) of all Calls in the Queue.  # noqa: E501

        :param average_wait_time: The average_wait_time of this QueueResultAllOf.  # noqa: E501
        :type: str
        """

        self._average_wait_time = average_wait_time

    @property
    def subresource_uris(self):
        """Gets the subresource_uris of this QueueResultAllOf.  # noqa: E501

        List of subresources for this Queue (which includes Queue members).  # noqa: E501

        :return: The subresource_uris of this QueueResultAllOf.  # noqa: E501
        :rtype: object
        """
        return self._subresource_uris

    @subresource_uris.setter
    def subresource_uris(self, subresource_uris):
        """Sets the subresource_uris of this QueueResultAllOf.

        List of subresources for this Queue (which includes Queue members).  # noqa: E501

        :param subresource_uris: The subresource_uris of this QueueResultAllOf.  # noqa: E501
        :type: object
        """

        self._subresource_uris = subresource_uris

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.to_camel_case(attr)
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
            elif value is None:
                continue
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, QueueResultAllOf):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, QueueResultAllOf):
            return True

        return self.to_dict() != other.to_dict()

    def to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
