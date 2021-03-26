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

class NetworkInterfacePerformanceFc(object):
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'received_bytes_per_sec': 'int',
        'received_crc_errors_per_sec': 'int',
        'received_frames_per_sec': 'int',
        'received_link_failures_per_sec': 'int',
        'received_loss_of_signal_per_sec': 'int',
        'received_loss_of_sync_per_sec': 'int',
        'total_errors_per_sec': 'int',
        'transmitted_bytes_per_sec': 'int',
        'transmitted_frames_per_sec': 'int',
        'transmitted_invalid_words_per_sec': 'int'
    }

    attribute_map = {
        'received_bytes_per_sec': 'received_bytes_per_sec',
        'received_crc_errors_per_sec': 'received_crc_errors_per_sec',
        'received_frames_per_sec': 'received_frames_per_sec',
        'received_link_failures_per_sec': 'received_link_failures_per_sec',
        'received_loss_of_signal_per_sec': 'received_loss_of_signal_per_sec',
        'received_loss_of_sync_per_sec': 'received_loss_of_sync_per_sec',
        'total_errors_per_sec': 'total_errors_per_sec',
        'transmitted_bytes_per_sec': 'transmitted_bytes_per_sec',
        'transmitted_frames_per_sec': 'transmitted_frames_per_sec',
        'transmitted_invalid_words_per_sec': 'transmitted_invalid_words_per_sec'
    }

    required_args = {
    }

    def __init__(
        self,
        received_bytes_per_sec=None,  # type: int
        received_crc_errors_per_sec=None,  # type: int
        received_frames_per_sec=None,  # type: int
        received_link_failures_per_sec=None,  # type: int
        received_loss_of_signal_per_sec=None,  # type: int
        received_loss_of_sync_per_sec=None,  # type: int
        total_errors_per_sec=None,  # type: int
        transmitted_bytes_per_sec=None,  # type: int
        transmitted_frames_per_sec=None,  # type: int
        transmitted_invalid_words_per_sec=None,  # type: int
    ):
        """
        Keyword args:
            received_bytes_per_sec (int): Bytes received per second.
            received_crc_errors_per_sec (int): Fibre Channel frame CRC errors per second.
            received_frames_per_sec (int): Fibre Channel frames received per second.
            received_link_failures_per_sec (int): Loss of connectivity errors per second.
            received_loss_of_signal_per_sec (int): Loss of signal errors on Fibre Channel port per second.
            received_loss_of_sync_per_sec (int): Loss of sync errors on Fibre Channel port per second.
            total_errors_per_sec (int): The sum of all reception and transmission errors per second.
            transmitted_bytes_per_sec (int): Bytes transmitted per second.
            transmitted_frames_per_sec (int): Fibre Channel frames transmitted per second.
            transmitted_invalid_words_per_sec (int): Bit errors in transmission word per second.
        """
        if received_bytes_per_sec is not None:
            self.received_bytes_per_sec = received_bytes_per_sec
        if received_crc_errors_per_sec is not None:
            self.received_crc_errors_per_sec = received_crc_errors_per_sec
        if received_frames_per_sec is not None:
            self.received_frames_per_sec = received_frames_per_sec
        if received_link_failures_per_sec is not None:
            self.received_link_failures_per_sec = received_link_failures_per_sec
        if received_loss_of_signal_per_sec is not None:
            self.received_loss_of_signal_per_sec = received_loss_of_signal_per_sec
        if received_loss_of_sync_per_sec is not None:
            self.received_loss_of_sync_per_sec = received_loss_of_sync_per_sec
        if total_errors_per_sec is not None:
            self.total_errors_per_sec = total_errors_per_sec
        if transmitted_bytes_per_sec is not None:
            self.transmitted_bytes_per_sec = transmitted_bytes_per_sec
        if transmitted_frames_per_sec is not None:
            self.transmitted_frames_per_sec = transmitted_frames_per_sec
        if transmitted_invalid_words_per_sec is not None:
            self.transmitted_invalid_words_per_sec = transmitted_invalid_words_per_sec

    def __setattr__(self, key, value):
        if key not in self.attribute_map:
            raise KeyError("Invalid key `{}` for `NetworkInterfacePerformanceFc`".format(key))
        if key == "received_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_crc_errors_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_crc_errors_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_frames_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_frames_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_link_failures_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_link_failures_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_loss_of_signal_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_loss_of_signal_per_sec`, must be a value greater than or equal to `0`")
        if key == "received_loss_of_sync_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `received_loss_of_sync_per_sec`, must be a value greater than or equal to `0`")
        if key == "total_errors_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `total_errors_per_sec`, must be a value greater than or equal to `0`")
        if key == "transmitted_bytes_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `transmitted_bytes_per_sec`, must be a value greater than or equal to `0`")
        if key == "transmitted_frames_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `transmitted_frames_per_sec`, must be a value greater than or equal to `0`")
        if key == "transmitted_invalid_words_per_sec" and value is not None:
            if value < 0:
                raise ValueError("Invalid value for `transmitted_invalid_words_per_sec`, must be a value greater than or equal to `0`")
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
        if issubclass(NetworkInterfacePerformanceFc, dict):
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
        if not isinstance(other, NetworkInterfacePerformanceFc):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
