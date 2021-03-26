# coding: utf-8

"""
    Pure1 Public REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.pure1.Pure1_1_1 import models

class Subscription(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'as_of': 'int',
        'id': 'str',
        'name': 'str',
        'expiration_date': 'int',
        'service': 'str',
        'start_date': 'int',
        'status': 'str'
    }

    attribute_map = {
        'as_of': '_as_of',
        'id': 'id',
        'name': 'name',
        'expiration_date': 'expiration_date',
        'service': 'service',
        'start_date': 'start_date',
        'status': 'status'
    }

    required_args = {
    }

    def __init__(
        self,
        as_of=None,  # type: int
        id=None,  # type: str
        name=None,  # type: str
        expiration_date=None,  # type: int
        service=None,  # type: str
        start_date=None,  # type: int
        status=None,  # type: str
    ):
        """
        Keyword args:
            as_of (int): The freshness of the data (timestamp in millis since epoch).
            id (str): A non-modifiable, globally unique ID chosen by the system.
            name (str): A non-modifiable, locally unique name chosen by the system.
            expiration_date (int): Date when the subscription expires. Represented as a timestamp of 00:00 on that date in UTC, in milliseconds since UNIX epoch.
            service (str): The service type of the subscription. Values include `Pure as-a-Service`, `FlashStack as a Service`, `Storage as a Service`, `PaaS (Block Storage Service)`, `PaaS (File and Object Storage Service)`, `PaaS (Data Protection Service)`, and `Pure1 Subscription`.
            start_date (int): Date when the subscription starts. Represented as a timestamp of 00:00 on that date in UTC, in milliseconds since UNIX epoch.
            status (str): Current status of the subscription. Values include `active`, `terminated`, `poc-expired`, and `signed`.
        """
        if as_of is not None:
            self.as_of = as_of
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if expiration_date is not None:
            self.expiration_date = expiration_date
        if service is not None:
            self.service = service
        if start_date is not None:
            self.start_date = start_date
        if status is not None:
            self.status = status

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Subscription`".format(key))
        self.__dict__[key] = value

    def __getattribute__(self, item):
        value = object.__getattribute__(self, item)
        if isinstance(value, Property):
            raise AttributeError
        else:
            return value

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            if hasattr(self, attr):
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
        if issubclass(Subscription, dict):
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
        if not isinstance(other, Subscription):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
