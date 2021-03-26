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

class Software(object):
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
        'details': 'str',
        'payload_id': 'str',
        'progress': 'float',
        'status': 'str',
        'upgrade_hops': 'list[str]',
        'version': 'str',
        'upgrade_plan': 'list[SoftwareUpgradePlan]'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'details': 'details',
        'payload_id': 'payload_id',
        'progress': 'progress',
        'status': 'status',
        'upgrade_hops': 'upgrade_hops',
        'version': 'version',
        'upgrade_plan': 'upgrade_plan'
    }

    required_args = {
    }

    def __init__(
        self,
        id=None,  # type: str
        name=None,  # type: str
        details=None,  # type: str
        payload_id=None,  # type: str
        progress=None,  # type: float
        status=None,  # type: str
        upgrade_hops=None,  # type: List[str]
        version=None,  # type: str
        upgrade_plan=None,  # type: List[models.SoftwareUpgradePlan]
    ):
        """
        Keyword args:
            id (str): A globally unique, system-generated ID. The ID cannot be modified.
            name (str): Name of the resource. The name cannot be modified.
            details (str): The detailed reason of the `status`.
            payload_id (str): A checksum hash referring to the update bundle.
            progress (float): The progress of the software upgrade. Displayed in decimal format.
            status (str): The status of the software package. Valid values are `available`, `downloaded`, `downloading`, `download_failed`, `checking`, `installing`, `paused`, `aborting`, `abort`, `canceled`, `partially_installed`, and `installed`. A status of `available` indicates that the package is available for download. This only applies if `automatic-download` is not enabled. A status of `downloaded` indicates that the package is downloaded and ready for installation. A status of `downloading` indicates that the package is currently downloading. A status of `download_failed` indicates that the download of the package failed. A status of `checking` indicates that the package is currently running in `check-only` mode. A status of `installing` indicates that the package is currently installing. A status of `paused` indicates that the upgrade is paused and waiting for user input to proceed. A status of `aborting` indicates that the upgrade is being aborted, due to an unrecoverable error or an `abort` command issued by the user. A status of `canceled` indicates that the upgrade has been canceled. A status of `partially_installed` indicates that the upgrade has been partially installed due to an `abort`. The array has been upgraded to an intermediate version and the `software` is no longer available for installation. A status of `installed` indicates that the upgrade has finished.
            upgrade_hops (list[str]): By which plan the upgrade will be conducted. The first element is the current version, the last element is the destination version, and the elements in between are intermediate versions.
            version (str): The version of the software package.
            upgrade_plan (list[SoftwareUpgradePlan]): A list of steps that are planned to run during the upgrade in an optimal scenario (i.e., all upgrade checks pass, no step is retried, and the upgrade is not aborted). Steps are listed in the order that they should occur.
        """
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if details is not None:
            self.details = details
        if payload_id is not None:
            self.payload_id = payload_id
        if progress is not None:
            self.progress = progress
        if status is not None:
            self.status = status
        if upgrade_hops is not None:
            self.upgrade_hops = upgrade_hops
        if version is not None:
            self.version = version
        if upgrade_plan is not None:
            self.upgrade_plan = upgrade_plan

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `Software`".format(key))
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
        if issubclass(Software, dict):
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
        if not isinstance(other, Software):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
