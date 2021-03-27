# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.8 Python SDK

    Pure Storage FlashBlade REST 1.8 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.8
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Dns(object):
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
        'domain': 'str',
        'nameservers': 'list[str]',
        'search': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'domain': 'domain',
        'nameservers': 'nameservers',
        'search': 'search'
    }

    def __init__(self, name=None, domain=None, nameservers=None, search=None):  # noqa: E501
        """Dns - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._domain = None
        self._nameservers = None
        self._search = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if domain is not None:
            self.domain = domain
        if nameservers is not None:
            self.nameservers = nameservers
        if search is not None:
            self.search = search

    @property
    def name(self):
        """Gets the name of this Dns.  # noqa: E501

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :return: The name of this Dns.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Dns.

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :param name: The name of this Dns.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def domain(self):
        """Gets the domain of this Dns.  # noqa: E501

        domain of the DNS configuration  # noqa: E501

        :return: The domain of this Dns.  # noqa: E501
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """Sets the domain of this Dns.

        domain of the DNS configuration  # noqa: E501

        :param domain: The domain of this Dns.  # noqa: E501
        :type: str
        """

        self._domain = domain

    @property
    def nameservers(self):
        """Gets the nameservers of this Dns.  # noqa: E501

        the IPs of nameservers  # noqa: E501

        :return: The nameservers of this Dns.  # noqa: E501
        :rtype: list[str]
        """
        return self._nameservers

    @nameservers.setter
    def nameservers(self, nameservers):
        """Sets the nameservers of this Dns.

        the IPs of nameservers  # noqa: E501

        :param nameservers: The nameservers of this Dns.  # noqa: E501
        :type: list[str]
        """

        self._nameservers = nameservers

    @property
    def search(self):
        """Gets the search of this Dns.  # noqa: E501

        the addresses for searching  # noqa: E501

        :return: The search of this Dns.  # noqa: E501
        :rtype: list[str]
        """
        return self._search

    @search.setter
    def search(self, search):
        """Sets the search of this Dns.

        the addresses for searching  # noqa: E501

        :param search: The search of this Dns.  # noqa: E501
        :type: list[str]
        """

        self._search = search

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
        if issubclass(Dns, dict):
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
        if not isinstance(other, Dns):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
