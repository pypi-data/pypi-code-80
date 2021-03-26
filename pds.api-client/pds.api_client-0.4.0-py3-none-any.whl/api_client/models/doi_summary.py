# coding: utf-8

"""
    Planetary Data System DOI Service API

    PDS API for managing DOI registration with OSTI service.  # noqa: E501

    The version of the OpenAPI document: 0.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pds.api_client.configuration import Configuration


class DoiSummary(object):
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
        'doi': 'str',
        'lidvid': 'str',
        'node': 'str',
        'submitter': 'str',
        'status': 'str',
        'update_date': 'datetime'
    }

    attribute_map = {
        'doi': 'doi',
        'lidvid': 'lidvid',
        'node': 'node',
        'submitter': 'submitter',
        'status': 'status',
        'update_date': 'update_date'
    }

    def __init__(self, doi=None, lidvid=None, node=None, submitter=None, status=None, update_date=None, local_vars_configuration=None):  # noqa: E501
        """DoiSummary - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._doi = None
        self._lidvid = None
        self._node = None
        self._submitter = None
        self._status = None
        self._update_date = None
        self.discriminator = None

        if doi is not None:
            self.doi = doi
        if lidvid is not None:
            self.lidvid = lidvid
        if node is not None:
            self.node = node
        if submitter is not None:
            self.submitter = submitter
        if status is not None:
            self.status = status
        if update_date is not None:
            self.update_date = update_date

    @property
    def doi(self):
        """Gets the doi of this DoiSummary.  # noqa: E501


        :return: The doi of this DoiSummary.  # noqa: E501
        :rtype: str
        """
        return self._doi

    @doi.setter
    def doi(self, doi):
        """Sets the doi of this DoiSummary.


        :param doi: The doi of this DoiSummary.  # noqa: E501
        :type: str
        """

        self._doi = doi

    @property
    def lidvid(self):
        """Gets the lidvid of this DoiSummary.  # noqa: E501


        :return: The lidvid of this DoiSummary.  # noqa: E501
        :rtype: str
        """
        return self._lidvid

    @lidvid.setter
    def lidvid(self, lidvid):
        """Sets the lidvid of this DoiSummary.


        :param lidvid: The lidvid of this DoiSummary.  # noqa: E501
        :type: str
        """

        self._lidvid = lidvid

    @property
    def node(self):
        """Gets the node of this DoiSummary.  # noqa: E501


        :return: The node of this DoiSummary.  # noqa: E501
        :rtype: str
        """
        return self._node

    @node.setter
    def node(self, node):
        """Sets the node of this DoiSummary.


        :param node: The node of this DoiSummary.  # noqa: E501
        :type: str
        """

        self._node = node

    @property
    def submitter(self):
        """Gets the submitter of this DoiSummary.  # noqa: E501


        :return: The submitter of this DoiSummary.  # noqa: E501
        :rtype: str
        """
        return self._submitter

    @submitter.setter
    def submitter(self, submitter):
        """Sets the submitter of this DoiSummary.


        :param submitter: The submitter of this DoiSummary.  # noqa: E501
        :type: str
        """

        self._submitter = submitter

    @property
    def status(self):
        """Gets the status of this DoiSummary.  # noqa: E501


        :return: The status of this DoiSummary.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DoiSummary.


        :param status: The status of this DoiSummary.  # noqa: E501
        :type: str
        """

        self._status = status

    @property
    def update_date(self):
        """Gets the update_date of this DoiSummary.  # noqa: E501


        :return: The update_date of this DoiSummary.  # noqa: E501
        :rtype: datetime
        """
        return self._update_date

    @update_date.setter
    def update_date(self, update_date):
        """Sets the update_date of this DoiSummary.


        :param update_date: The update_date of this DoiSummary.  # noqa: E501
        :type: datetime
        """

        self._update_date = update_date

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DoiSummary):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DoiSummary):
            return True

        return self.to_dict() != other.to_dict()
