# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.12 Python SDK

    Pure Storage FlashBlade REST 1.12 Python SDK. Compatible with REST API versions 1.0 - 1.12. Developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.12
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ApiClientPost(object):
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
        'max_role': 'FixedReferenceNoResourceType',
        'issuer': 'str',
        'public_key': 'str',
        'access_token_ttl_in_ms': 'int'
    }

    attribute_map = {
        'max_role': 'max_role',
        'issuer': 'issuer',
        'public_key': 'public_key',
        'access_token_ttl_in_ms': 'access_token_ttl_in_ms'
    }

    def __init__(self, max_role=None, issuer=None, public_key=None, access_token_ttl_in_ms=None):  # noqa: E501
        """ApiClientPost - a model defined in Swagger"""  # noqa: E501

        self._max_role = None
        self._issuer = None
        self._public_key = None
        self._access_token_ttl_in_ms = None
        self.discriminator = None

        if max_role is not None:
            self.max_role = max_role
        if issuer is not None:
            self.issuer = issuer
        if public_key is not None:
            self.public_key = public_key
        if access_token_ttl_in_ms is not None:
            self.access_token_ttl_in_ms = access_token_ttl_in_ms

    @property
    def max_role(self):
        """Gets the max_role of this ApiClientPost.  # noqa: E501

        The maximum role allowed for ID Tokens issued by this API client. The bearer of an access token will be authorized to perform actions within the intersection of this max_role and the role of the array user specified as the JWT sub (subject) claim. Valid max_role values are readonly, ops_admin, array_admin, and storage_admin. Users with the readonly (Read Only) role can perform operations that convey the state of the array. Read Only users cannot alter the state of the array. Users with the ops_admin (Ops Admin) role can perform the same operations as Read Only users plus enable and disable remote assistance sessions. Ops Admin users cannot alter the state of the array. Users with the storage_admin (Storage Admin) role can perform the same operations as Read Only users plus storage related operations, such as administering volumes, hosts, and host groups. Storage Admin users cannot perform operations that deal with global and system configurations. Users with the array_admin (Array Admin) role can perform the same operations as Storage Admin users plus array-wide changes dealing with global and system configurations. In other words, Array Admin users can perform all operations. Modifiable  # noqa: E501

        :return: The max_role of this ApiClientPost.  # noqa: E501
        :rtype: FixedReferenceNoResourceType
        """
        return self._max_role

    @max_role.setter
    def max_role(self, max_role):
        """Sets the max_role of this ApiClientPost.

        The maximum role allowed for ID Tokens issued by this API client. The bearer of an access token will be authorized to perform actions within the intersection of this max_role and the role of the array user specified as the JWT sub (subject) claim. Valid max_role values are readonly, ops_admin, array_admin, and storage_admin. Users with the readonly (Read Only) role can perform operations that convey the state of the array. Read Only users cannot alter the state of the array. Users with the ops_admin (Ops Admin) role can perform the same operations as Read Only users plus enable and disable remote assistance sessions. Ops Admin users cannot alter the state of the array. Users with the storage_admin (Storage Admin) role can perform the same operations as Read Only users plus storage related operations, such as administering volumes, hosts, and host groups. Storage Admin users cannot perform operations that deal with global and system configurations. Users with the array_admin (Array Admin) role can perform the same operations as Storage Admin users plus array-wide changes dealing with global and system configurations. In other words, Array Admin users can perform all operations. Modifiable  # noqa: E501

        :param max_role: The max_role of this ApiClientPost.  # noqa: E501
        :type: FixedReferenceNoResourceType
        """

        self._max_role = max_role

    @property
    def issuer(self):
        """Gets the issuer of this ApiClientPost.  # noqa: E501

        The name of the identity provider that will be issuing ID Tokens for this API client. The iss claim in the JWT issued must match this string. If not specified, defaults to the API client name. Modifiable  # noqa: E501

        :return: The issuer of this ApiClientPost.  # noqa: E501
        :rtype: str
        """
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        """Sets the issuer of this ApiClientPost.

        The name of the identity provider that will be issuing ID Tokens for this API client. The iss claim in the JWT issued must match this string. If not specified, defaults to the API client name. Modifiable  # noqa: E501

        :param issuer: The issuer of this ApiClientPost.  # noqa: E501
        :type: str
        """

        self._issuer = issuer

    @property
    def public_key(self):
        """Gets the public_key of this ApiClientPost.  # noqa: E501

        The API client’s PEM formatted (Base64 encoded) RSA public key. It must include the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- lines. Modifiable  # noqa: E501

        :return: The public_key of this ApiClientPost.  # noqa: E501
        :rtype: str
        """
        return self._public_key

    @public_key.setter
    def public_key(self, public_key):
        """Sets the public_key of this ApiClientPost.

        The API client’s PEM formatted (Base64 encoded) RSA public key. It must include the -----BEGIN PUBLIC KEY----- and -----END PUBLIC KEY----- lines. Modifiable  # noqa: E501

        :param public_key: The public_key of this ApiClientPost.  # noqa: E501
        :type: str
        """

        self._public_key = public_key

    @property
    def access_token_ttl_in_ms(self):
        """Gets the access_token_ttl_in_ms of this ApiClientPost.  # noqa: E501

        The TTL (Time To Live) duration for which the exchanged access token is valid. Measured in milliseconds. If not specified, defaults to 86400000. Modifiable  # noqa: E501

        :return: The access_token_ttl_in_ms of this ApiClientPost.  # noqa: E501
        :rtype: int
        """
        return self._access_token_ttl_in_ms

    @access_token_ttl_in_ms.setter
    def access_token_ttl_in_ms(self, access_token_ttl_in_ms):
        """Sets the access_token_ttl_in_ms of this ApiClientPost.

        The TTL (Time To Live) duration for which the exchanged access token is valid. Measured in milliseconds. If not specified, defaults to 86400000. Modifiable  # noqa: E501

        :param access_token_ttl_in_ms: The access_token_ttl_in_ms of this ApiClientPost.  # noqa: E501
        :type: int
        """

        self._access_token_ttl_in_ms = access_token_ttl_in_ms

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
        if issubclass(ApiClientPost, dict):
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
        if not isinstance(other, ApiClientPost):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
