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


class Keytab(object):
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
        'encryption_type': 'str',
        'fqdn': 'str',
        'kvno': 'int',
        'prefix': 'str',
        'principal': 'str',
        'realm': 'str',
        'suffix': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'encryption_type': 'encryption_type',
        'fqdn': 'fqdn',
        'kvno': 'kvno',
        'prefix': 'prefix',
        'principal': 'principal',
        'realm': 'realm',
        'suffix': 'suffix'
    }

    def __init__(self, id=None, name=None, encryption_type=None, fqdn=None, kvno=None, prefix=None, principal=None, realm=None, suffix=None):  # noqa: E501
        """Keytab - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._name = None
        self._encryption_type = None
        self._fqdn = None
        self._kvno = None
        self._prefix = None
        self._principal = None
        self._realm = None
        self._suffix = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if encryption_type is not None:
            self.encryption_type = encryption_type
        if fqdn is not None:
            self.fqdn = fqdn
        if kvno is not None:
            self.kvno = kvno
        if prefix is not None:
            self.prefix = prefix
        if principal is not None:
            self.principal = principal
        if realm is not None:
            self.realm = realm
        if suffix is not None:
            self.suffix = suffix

    @property
    def id(self):
        """Gets the id of this Keytab.  # noqa: E501

        A non-modifiable, globally unique ID chosen by the system.  # noqa: E501

        :return: The id of this Keytab.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Keytab.

        A non-modifiable, globally unique ID chosen by the system.  # noqa: E501

        :param id: The id of this Keytab.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Keytab.  # noqa: E501

        The name of the object (e.g., a file system or snapshot).  # noqa: E501

        :return: The name of this Keytab.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Keytab.

        The name of the object (e.g., a file system or snapshot).  # noqa: E501

        :param name: The name of this Keytab.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def encryption_type(self):
        """Gets the encryption_type of this Keytab.  # noqa: E501

        The encryption type used by the kerberos domain controller to generate the keytab.  # noqa: E501

        :return: The encryption_type of this Keytab.  # noqa: E501
        :rtype: str
        """
        return self._encryption_type

    @encryption_type.setter
    def encryption_type(self, encryption_type):
        """Sets the encryption_type of this Keytab.

        The encryption type used by the kerberos domain controller to generate the keytab.  # noqa: E501

        :param encryption_type: The encryption_type of this Keytab.  # noqa: E501
        :type: str
        """

        self._encryption_type = encryption_type

    @property
    def fqdn(self):
        """Gets the fqdn of this Keytab.  # noqa: E501

        The fully qualified domain name to which the keytab was issued.  # noqa: E501

        :return: The fqdn of this Keytab.  # noqa: E501
        :rtype: str
        """
        return self._fqdn

    @fqdn.setter
    def fqdn(self, fqdn):
        """Sets the fqdn of this Keytab.

        The fully qualified domain name to which the keytab was issued.  # noqa: E501

        :param fqdn: The fqdn of this Keytab.  # noqa: E501
        :type: str
        """

        self._fqdn = fqdn

    @property
    def kvno(self):
        """Gets the kvno of this Keytab.  # noqa: E501

        The key version number of the key used to generate the keytab.  # noqa: E501

        :return: The kvno of this Keytab.  # noqa: E501
        :rtype: int
        """
        return self._kvno

    @kvno.setter
    def kvno(self, kvno):
        """Sets the kvno of this Keytab.

        The key version number of the key used to generate the keytab.  # noqa: E501

        :param kvno: The kvno of this Keytab.  # noqa: E501
        :type: int
        """

        self._kvno = kvno

    @property
    def prefix(self):
        """Gets the prefix of this Keytab.  # noqa: E501

        The prefix in the name of the keytab object. This is the same for all keytab objects created from a single keytab file. The name of a keytab entry is created in the format `<prefix>.<suffix>` for all entries.  # noqa: E501

        :return: The prefix of this Keytab.  # noqa: E501
        :rtype: str
        """
        return self._prefix

    @prefix.setter
    def prefix(self, prefix):
        """Sets the prefix of this Keytab.

        The prefix in the name of the keytab object. This is the same for all keytab objects created from a single keytab file. The name of a keytab entry is created in the format `<prefix>.<suffix>` for all entries.  # noqa: E501

        :param prefix: The prefix of this Keytab.  # noqa: E501
        :type: str
        """

        self._prefix = prefix

    @property
    def principal(self):
        """Gets the principal of this Keytab.  # noqa: E501

        The service name for which the keytab was issued.  # noqa: E501

        :return: The principal of this Keytab.  # noqa: E501
        :rtype: str
        """
        return self._principal

    @principal.setter
    def principal(self, principal):
        """Sets the principal of this Keytab.

        The service name for which the keytab was issued.  # noqa: E501

        :param principal: The principal of this Keytab.  # noqa: E501
        :type: str
        """

        self._principal = principal

    @property
    def realm(self):
        """Gets the realm of this Keytab.  # noqa: E501

        The kerberos realm that issued the keytab.  # noqa: E501

        :return: The realm of this Keytab.  # noqa: E501
        :rtype: str
        """
        return self._realm

    @realm.setter
    def realm(self, realm):
        """Sets the realm of this Keytab.

        The kerberos realm that issued the keytab.  # noqa: E501

        :param realm: The realm of this Keytab.  # noqa: E501
        :type: str
        """

        self._realm = realm

    @property
    def suffix(self):
        """Gets the suffix of this Keytab.  # noqa: E501

        The suffix in the name of the keytab object, determined at creation time using the slot number of the keytab entry in a file and the number of existing entries with the same prefix. The name of a keytab entry is created in the format `<prefix>.<suffix>` for all entries.  # noqa: E501

        :return: The suffix of this Keytab.  # noqa: E501
        :rtype: int
        """
        return self._suffix

    @suffix.setter
    def suffix(self, suffix):
        """Sets the suffix of this Keytab.

        The suffix in the name of the keytab object, determined at creation time using the slot number of the keytab entry in a file and the number of existing entries with the same prefix. The name of a keytab entry is created in the format `<prefix>.<suffix>` for all entries.  # noqa: E501

        :param suffix: The suffix of this Keytab.  # noqa: E501
        :type: int
        """

        self._suffix = suffix

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
        if issubclass(Keytab, dict):
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
        if not isinstance(other, Keytab):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
