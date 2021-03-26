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


class CertificateUse(object):
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
        'id': 'str',
        'name': 'str',
        'group': 'FixedReferenceWithId',
        'use': 'FixedReferenceWithRemote'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'group': 'group',
        'use': 'use'
    }

    def __init__(self, id=None, name=None, group=None, use=None):  # noqa: E501
        """CertificateUse - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._name = None
        self._group = None
        self._use = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if group is not None:
            self.group = group
        if use is not None:
            self.use = use

    @property
    def id(self):
        """Gets the id of this CertificateUse.  # noqa: E501

        A non-modifiable, globally unique ID chosen by the system.  # noqa: E501

        :return: The id of this CertificateUse.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this CertificateUse.

        A non-modifiable, globally unique ID chosen by the system.  # noqa: E501

        :param id: The id of this CertificateUse.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this CertificateUse.  # noqa: E501

        The name of the object (e.g., a file system or snapshot).  # noqa: E501

        :return: The name of this CertificateUse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CertificateUse.

        The name of the object (e.g., a file system or snapshot).  # noqa: E501

        :param name: The name of this CertificateUse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def group(self):
        """Gets the group of this CertificateUse.  # noqa: E501

        A reference to a certificate-group that is being used, if any, where this certificate is a member of the certificate-group. This field is null if the referenced use object is not using a group, but is rather using this certificate directly.  # noqa: E501

        :return: The group of this CertificateUse.  # noqa: E501
        :rtype: FixedReferenceWithId
        """
        return self._group

    @group.setter
    def group(self, group):
        """Sets the group of this CertificateUse.

        A reference to a certificate-group that is being used, if any, where this certificate is a member of the certificate-group. This field is null if the referenced use object is not using a group, but is rather using this certificate directly.  # noqa: E501

        :param group: The group of this CertificateUse.  # noqa: E501
        :type: FixedReferenceWithId
        """

        self._group = group

    @property
    def use(self):
        """Gets the use of this CertificateUse.  # noqa: E501

        A reference to an object using this certificate.  # noqa: E501

        :return: The use of this CertificateUse.  # noqa: E501
        :rtype: FixedReferenceWithRemote
        """
        return self._use

    @use.setter
    def use(self, use):
        """Sets the use of this CertificateUse.

        A reference to an object using this certificate.  # noqa: E501

        :param use: The use of this CertificateUse.  # noqa: E501
        :type: FixedReferenceWithRemote
        """

        self._use = use

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
        if issubclass(CertificateUse, dict):
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
        if not isinstance(other, CertificateUse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
