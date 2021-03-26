# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.4 Python SDK

    Pure Storage FlashBlade REST 1.4 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.4
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Blade(object):
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
        'details': 'str',
        'raw_capacity': 'int',
        'target': 'str',
        'progress': 'float',
        'status': 'str'
    }

    attribute_map = {
        'name': 'name',
        'details': 'details',
        'raw_capacity': 'raw_capacity',
        'target': 'target',
        'progress': 'progress',
        'status': 'status'
    }

    def __init__(self, name=None, details=None, raw_capacity=None, target=None, progress=None, status=None):  # noqa: E501
        """Blade - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._details = None
        self._raw_capacity = None
        self._target = None
        self._progress = None
        self._status = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if details is not None:
            self.details = details
        if raw_capacity is not None:
            self.raw_capacity = raw_capacity
        if target is not None:
            self.target = target
        if progress is not None:
            self.progress = progress
        if status is not None:
            self.status = status

    @property
    def name(self):
        """Gets the name of this Blade.  # noqa: E501

        blade name  # noqa: E501

        :return: The name of this Blade.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Blade.

        blade name  # noqa: E501

        :param name: The name of this Blade.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def details(self):
        """Gets the details of this Blade.  # noqa: E501

        blade details  # noqa: E501

        :return: The details of this Blade.  # noqa: E501
        :rtype: str
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this Blade.

        blade details  # noqa: E501

        :param details: The details of this Blade.  # noqa: E501
        :type: str
        """

        self._details = details

    @property
    def raw_capacity(self):
        """Gets the raw_capacity of this Blade.  # noqa: E501

        blade capacity in bytes  # noqa: E501

        :return: The raw_capacity of this Blade.  # noqa: E501
        :rtype: int
        """
        return self._raw_capacity

    @raw_capacity.setter
    def raw_capacity(self, raw_capacity):
        """Sets the raw_capacity of this Blade.

        blade capacity in bytes  # noqa: E501

        :param raw_capacity: The raw_capacity of this Blade.  # noqa: E501
        :type: int
        """

        self._raw_capacity = raw_capacity

    @property
    def target(self):
        """Gets the target of this Blade.  # noqa: E501

        evacuation target  # noqa: E501

        :return: The target of this Blade.  # noqa: E501
        :rtype: str
        """
        return self._target

    @target.setter
    def target(self, target):
        """Sets the target of this Blade.

        evacuation target  # noqa: E501

        :param target: The target of this Blade.  # noqa: E501
        :type: str
        """

        self._target = target

    @property
    def progress(self):
        """Gets the progress of this Blade.  # noqa: E501

        current operation progress  # noqa: E501

        :return: The progress of this Blade.  # noqa: E501
        :rtype: float
        """
        return self._progress

    @progress.setter
    def progress(self, progress):
        """Sets the progress of this Blade.

        current operation progress  # noqa: E501

        :param progress: The progress of this Blade.  # noqa: E501
        :type: float
        """

        self._progress = progress

    @property
    def status(self):
        """Gets the status of this Blade.  # noqa: E501

        blade status  # noqa: E501

        :return: The status of this Blade.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Blade.

        blade status  # noqa: E501

        :param status: The status of this Blade.  # noqa: E501
        :type: str
        """

        self._status = status

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
        if issubclass(Blade, dict):
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
        if not isinstance(other, Blade):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
