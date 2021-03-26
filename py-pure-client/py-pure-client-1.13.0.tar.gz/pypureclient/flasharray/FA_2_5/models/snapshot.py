# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.5
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_5 import models

class Snapshot(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'created': 'int',
        'destroyed': 'bool',
        'pod': 'FixedReference',
        'provisioned': 'int',
        'source': 'FixedReference',
        'suffix': 'str',
        'time_remaining': 'int'
    }

    attribute_map = {
        'created': 'created',
        'destroyed': 'destroyed',
        'pod': 'pod',
        'provisioned': 'provisioned',
        'source': 'source',
        'suffix': 'suffix',
        'time_remaining': 'time_remaining'
    }

    required_args = {
    }

    def __init__(
        self,
        created=None,  # type: int
        destroyed=None,  # type: bool
        pod=None,  # type: models.FixedReference
        provisioned=None,  # type: int
        source=None,  # type: models.FixedReference
        suffix=None,  # type: str
        time_remaining=None,  # type: int
    ):
        """
        Keyword args:
            created (int): The snapshot creation time. Measured in milliseconds since the UNIX epoch.
            destroyed (bool): Returns a value of `true` if the snapshot has been destroyed and is pending eradication. The `time_remaining` value displays the amount of time left until the destroyed volume snapshot is permanently eradicated. Before the `time_remaining` period has elapsed, the destroyed volume snapshot can be recovered by setting `destroyed=false`. Once the `time_remaining` period has elapsed, the volume snapshot is permanently eradicated and can no longer be recovered.
            pod (FixedReference): A reference to the pod.
            provisioned (int): The provisioned space of the snapshot. Measured in bytes.
            source (FixedReference): The volume from which this snapshot was taken.
            suffix (str): The suffix that is appended to the `source_name` value to generate the full volume snapshot name in the form `VOL.SUFFIX`. If the suffix is not specified, the system constructs the snapshot name in the form `VOL.NNN`, where `VOL` is the volume name, and `NNN` is a monotonically increasing number.
            time_remaining (int): The amount of time left until the destroyed snapshot is permanently eradicated. Measured in milliseconds. Before the `time_remaining` period has elapsed, the destroyed snapshot can be recovered by setting `destroyed=false`.
        """
        if created is not None:
            self.created = created
        if destroyed is not None:
            self.destroyed = destroyed
        if pod is not None:
            self.pod = pod
        if provisioned is not None:
            self.provisioned = provisioned
        if source is not None:
            self.source = source
        if suffix is not None:
            self.suffix = suffix
        if time_remaining is not None:
            self.time_remaining = time_remaining

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Snapshot`".format(key))
        if key == "provisioned" and value is not None:
            if value > 4503599627370496:
                raise ValueError("Invalid value for `provisioned`, value must be less than or equal to `4503599627370496`")
            if value < 1048576:
                raise ValueError("Invalid value for `provisioned`, must be a value greater than or equal to `1048576`")
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
        if issubclass(Snapshot, dict):
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
        if not isinstance(other, Snapshot):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
