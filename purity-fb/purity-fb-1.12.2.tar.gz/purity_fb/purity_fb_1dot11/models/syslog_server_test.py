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


class SyslogServerTest(object):
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
        'component_address': 'str',
        'component_name': 'str',
        'description': 'str',
        'destination': 'str',
        'details': 'str',
        'success': 'bool',
        'test_type': 'str'
    }

    attribute_map = {
        'component_address': 'component_address',
        'component_name': 'component_name',
        'description': 'description',
        'destination': 'destination',
        'details': 'details',
        'success': 'success',
        'test_type': 'test_type'
    }

    def __init__(self, component_address=None, component_name=None, description=None, destination=None, details=None, success=None, test_type=None):  # noqa: E501
        """SyslogServerTest - a model defined in Swagger"""  # noqa: E501

        self._component_address = None
        self._component_name = None
        self._description = None
        self._destination = None
        self._details = None
        self._success = None
        self._test_type = None
        self.discriminator = None

        if component_address is not None:
            self.component_address = component_address
        if component_name is not None:
            self.component_name = component_name
        if description is not None:
            self.description = description
        if destination is not None:
            self.destination = destination
        if details is not None:
            self.details = details
        if success is not None:
            self.success = success
        if test_type is not None:
            self.test_type = test_type

    @property
    def component_address(self):
        """Gets the component_address of this SyslogServerTest.  # noqa: E501

        Address of the component running the test.  # noqa: E501

        :return: The component_address of this SyslogServerTest.  # noqa: E501
        :rtype: str
        """
        return self._component_address

    @component_address.setter
    def component_address(self, component_address):
        """Sets the component_address of this SyslogServerTest.

        Address of the component running the test.  # noqa: E501

        :param component_address: The component_address of this SyslogServerTest.  # noqa: E501
        :type: str
        """

        self._component_address = component_address

    @property
    def component_name(self):
        """Gets the component_name of this SyslogServerTest.  # noqa: E501

        Name of the component running the test.  # noqa: E501

        :return: The component_name of this SyslogServerTest.  # noqa: E501
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name):
        """Sets the component_name of this SyslogServerTest.

        Name of the component running the test.  # noqa: E501

        :param component_name: The component_name of this SyslogServerTest.  # noqa: E501
        :type: str
        """

        self._component_name = component_name

    @property
    def description(self):
        """Gets the description of this SyslogServerTest.  # noqa: E501

        What the test is doing.  # noqa: E501

        :return: The description of this SyslogServerTest.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this SyslogServerTest.

        What the test is doing.  # noqa: E501

        :param description: The description of this SyslogServerTest.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def destination(self):
        """Gets the destination of this SyslogServerTest.  # noqa: E501

        The URI of the target syslog server being tested.  # noqa: E501

        :return: The destination of this SyslogServerTest.  # noqa: E501
        :rtype: str
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """Sets the destination of this SyslogServerTest.

        The URI of the target syslog server being tested.  # noqa: E501

        :param destination: The destination of this SyslogServerTest.  # noqa: E501
        :type: str
        """

        self._destination = destination

    @property
    def details(self):
        """Gets the details of this SyslogServerTest.  # noqa: E501

        The output of the test.  # noqa: E501

        :return: The details of this SyslogServerTest.  # noqa: E501
        :rtype: str
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this SyslogServerTest.

        The output of the test.  # noqa: E501

        :param details: The details of this SyslogServerTest.  # noqa: E501
        :type: str
        """

        self._details = details

    @property
    def success(self):
        """Gets the success of this SyslogServerTest.  # noqa: E501

        Returns a value of `true` if the specified test succeeded. Returns a value of `false` if the specified test failed.  # noqa: E501

        :return: The success of this SyslogServerTest.  # noqa: E501
        :rtype: bool
        """
        return self._success

    @success.setter
    def success(self, success):
        """Sets the success of this SyslogServerTest.

        Returns a value of `true` if the specified test succeeded. Returns a value of `false` if the specified test failed.  # noqa: E501

        :param success: The success of this SyslogServerTest.  # noqa: E501
        :type: bool
        """

        self._success = success

    @property
    def test_type(self):
        """Gets the test_type of this SyslogServerTest.  # noqa: E501

        Displays the type of test being performed.  The returned values are determined by the syslog connection being tested and its configuration. Possible values include `connecting` and `message-sending`.  # noqa: E501

        :return: The test_type of this SyslogServerTest.  # noqa: E501
        :rtype: str
        """
        return self._test_type

    @test_type.setter
    def test_type(self, test_type):
        """Sets the test_type of this SyslogServerTest.

        Displays the type of test being performed.  The returned values are determined by the syslog connection being tested and its configuration. Possible values include `connecting` and `message-sending`.  # noqa: E501

        :param test_type: The test_type of this SyslogServerTest.  # noqa: E501
        :type: str
        """

        self._test_type = test_type

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
        if issubclass(SyslogServerTest, dict):
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
        if not isinstance(other, SyslogServerTest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
