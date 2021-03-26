# coding: utf-8

"""
    Planetary Data System API

    Federated PDS API which provides actionable end points standardized between the different nodes.   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Contact: pds-operator@jpl.nasa.gov
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pds.api_client.configuration import Configuration


class Metadata(object):
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
        'creation_date_time': 'str',
        'update_date_time': 'str',
        'version': 'str',
        'label_url': 'str'
    }

    attribute_map = {
        'creation_date_time': 'creation_date_time',
        'update_date_time': 'update_date_time',
        'version': 'version',
        'label_url': 'label_url'
    }

    def __init__(self, creation_date_time=None, update_date_time=None, version=None, label_url=None, local_vars_configuration=None):  # noqa: E501
        """Metadata - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._creation_date_time = None
        self._update_date_time = None
        self._version = None
        self._label_url = None
        self.discriminator = None

        if creation_date_time is not None:
            self.creation_date_time = creation_date_time
        if update_date_time is not None:
            self.update_date_time = update_date_time
        if version is not None:
            self.version = version
        self.label_url = label_url

    @property
    def creation_date_time(self):
        """Gets the creation_date_time of this Metadata.  # noqa: E501


        :return: The creation_date_time of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._creation_date_time

    @creation_date_time.setter
    def creation_date_time(self, creation_date_time):
        """Sets the creation_date_time of this Metadata.


        :param creation_date_time: The creation_date_time of this Metadata.  # noqa: E501
        :type: str
        """

        self._creation_date_time = creation_date_time

    @property
    def update_date_time(self):
        """Gets the update_date_time of this Metadata.  # noqa: E501


        :return: The update_date_time of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._update_date_time

    @update_date_time.setter
    def update_date_time(self, update_date_time):
        """Sets the update_date_time of this Metadata.


        :param update_date_time: The update_date_time of this Metadata.  # noqa: E501
        :type: str
        """

        self._update_date_time = update_date_time

    @property
    def version(self):
        """Gets the version of this Metadata.  # noqa: E501


        :return: The version of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Metadata.


        :param version: The version of this Metadata.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def label_url(self):
        """Gets the label_url of this Metadata.  # noqa: E501


        :return: The label_url of this Metadata.  # noqa: E501
        :rtype: str
        """
        return self._label_url

    @label_url.setter
    def label_url(self, label_url):
        """Sets the label_url of this Metadata.


        :param label_url: The label_url of this Metadata.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and label_url is None:  # noqa: E501
            raise ValueError("Invalid value for `label_url`, must not be `None`")  # noqa: E501

        self._label_url = label_url

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
        if not isinstance(other, Metadata):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Metadata):
            return True

        return self.to_dict() != other.to_dict()
