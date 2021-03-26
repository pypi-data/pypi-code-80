# coding: utf-8

"""
    FlashArray REST API

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 2.3
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re

import six
import typing

from ....properties import Property
if typing.TYPE_CHECKING:
    from pypureclient.flasharray.FA_2_3 import models

class Offload(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'azure': 'OffloadAzure',
        'google_cloud': 'OffloadGoogleCloud',
        'nfs': 'OffloadNfs',
        's3': 'OffloadS3',
        'name': 'str',
        'protocol': 'str',
        'target_id': 'str',
        'space': 'Space',
        'status': 'str'
    }

    attribute_map = {
        'azure': 'azure',
        'google_cloud': 'google-cloud',
        'nfs': 'nfs',
        's3': 's3',
        'name': 'name',
        'protocol': 'protocol',
        'target_id': 'target_id',
        'space': 'space',
        'status': 'status'
    }

    required_args = {
    }

    def __init__(
        self,
        azure=None,  # type: models.OffloadAzure
        google_cloud=None,  # type: models.OffloadGoogleCloud
        nfs=None,  # type: models.OffloadNfs
        s3=None,  # type: models.OffloadS3
        name=None,  # type: str
        protocol=None,  # type: str
        target_id=None,  # type: str
        space=None,  # type: models.Space
        status=None,  # type: str
    ):
        """
        Keyword args:
            azure (OffloadAzure): Microsoft Azure Blob storage settings.
            google_cloud (OffloadGoogleCloud): Google Cloud Storage settings.
            nfs (OffloadNfs): NFS settings.
            s3 (OffloadS3): S3 settings.
            name (str): A user-specified name. The name must be locally unique and can be changed.
            protocol (str): Type of offload. Valid values include `azure`, `google-cloud`, `nfs`, and `s3`.
            target_id (str): Unique ID for the offload target. When multiple connections to one offload target are created, they each have distinct IDs but share the same `target_id`.
            space (Space)
            status (str): Offload status. Valid values are `connecting`, `connected`, `disconnecting`, `not connected`, and `scanning`.
        """
        if azure is not None:
            self.azure = azure
        if google_cloud is not None:
            self.google_cloud = google_cloud
        if nfs is not None:
            self.nfs = nfs
        if s3 is not None:
            self.s3 = s3
        if name is not None:
            self.name = name
        if protocol is not None:
            self.protocol = protocol
        if target_id is not None:
            self.target_id = target_id
        if space is not None:
            self.space = space
        if status is not None:
            self.status = status

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Offload`".format(key))
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
        if issubclass(Offload, dict):
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
        if not isinstance(other, Offload):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
