# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.8 Python SDK

    Pure Storage FlashBlade REST 1.8 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.8
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class BucketS3Performance(object):
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
        'others_per_sec': 'int',
        'read_buckets_per_sec': 'int',
        'read_objects_per_sec': 'int',
        'write_buckets_per_sec': 'int',
        'write_objects_per_sec': 'int',
        'time': 'int',
        'usec_per_other_op': 'int',
        'usec_per_read_bucket_op': 'int',
        'usec_per_read_object_op': 'int',
        'usec_per_write_bucket_op': 'int',
        'usec_per_write_object_op': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'others_per_sec': 'others_per_sec',
        'read_buckets_per_sec': 'read_buckets_per_sec',
        'read_objects_per_sec': 'read_objects_per_sec',
        'write_buckets_per_sec': 'write_buckets_per_sec',
        'write_objects_per_sec': 'write_objects_per_sec',
        'time': 'time',
        'usec_per_other_op': 'usec_per_other_op',
        'usec_per_read_bucket_op': 'usec_per_read_bucket_op',
        'usec_per_read_object_op': 'usec_per_read_object_op',
        'usec_per_write_bucket_op': 'usec_per_write_bucket_op',
        'usec_per_write_object_op': 'usec_per_write_object_op'
    }

    def __init__(self, id=None, name=None, others_per_sec=None, read_buckets_per_sec=None, read_objects_per_sec=None, write_buckets_per_sec=None, write_objects_per_sec=None, time=None, usec_per_other_op=None, usec_per_read_bucket_op=None, usec_per_read_object_op=None, usec_per_write_bucket_op=None, usec_per_write_object_op=None):  # noqa: E501
        """BucketS3Performance - a model defined in Swagger"""  # noqa: E501

        self._id = None
        self._name = None
        self._others_per_sec = None
        self._read_buckets_per_sec = None
        self._read_objects_per_sec = None
        self._write_buckets_per_sec = None
        self._write_objects_per_sec = None
        self._time = None
        self._usec_per_other_op = None
        self._usec_per_read_bucket_op = None
        self._usec_per_read_object_op = None
        self._usec_per_write_bucket_op = None
        self._usec_per_write_object_op = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if others_per_sec is not None:
            self.others_per_sec = others_per_sec
        if read_buckets_per_sec is not None:
            self.read_buckets_per_sec = read_buckets_per_sec
        if read_objects_per_sec is not None:
            self.read_objects_per_sec = read_objects_per_sec
        if write_buckets_per_sec is not None:
            self.write_buckets_per_sec = write_buckets_per_sec
        if write_objects_per_sec is not None:
            self.write_objects_per_sec = write_objects_per_sec
        if time is not None:
            self.time = time
        if usec_per_other_op is not None:
            self.usec_per_other_op = usec_per_other_op
        if usec_per_read_bucket_op is not None:
            self.usec_per_read_bucket_op = usec_per_read_bucket_op
        if usec_per_read_object_op is not None:
            self.usec_per_read_object_op = usec_per_read_object_op
        if usec_per_write_bucket_op is not None:
            self.usec_per_write_bucket_op = usec_per_write_bucket_op
        if usec_per_write_object_op is not None:
            self.usec_per_write_object_op = usec_per_write_object_op

    @property
    def id(self):
        """Gets the id of this BucketS3Performance.  # noqa: E501

        A non-modifiable, globally unique ID chosen by the system.  # noqa: E501

        :return: The id of this BucketS3Performance.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BucketS3Performance.

        A non-modifiable, globally unique ID chosen by the system.  # noqa: E501

        :param id: The id of this BucketS3Performance.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this BucketS3Performance.  # noqa: E501

        The name of the object (e.g., a file system or snapshot).  # noqa: E501

        :return: The name of this BucketS3Performance.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this BucketS3Performance.

        The name of the object (e.g., a file system or snapshot).  # noqa: E501

        :param name: The name of this BucketS3Performance.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def others_per_sec(self):
        """Gets the others_per_sec of this BucketS3Performance.  # noqa: E501

        Other operations processed per second.  # noqa: E501

        :return: The others_per_sec of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._others_per_sec

    @others_per_sec.setter
    def others_per_sec(self, others_per_sec):
        """Sets the others_per_sec of this BucketS3Performance.

        Other operations processed per second.  # noqa: E501

        :param others_per_sec: The others_per_sec of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if others_per_sec is not None and others_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `others_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._others_per_sec = others_per_sec

    @property
    def read_buckets_per_sec(self):
        """Gets the read_buckets_per_sec of this BucketS3Performance.  # noqa: E501

        Read buckets requests processed per second.  # noqa: E501

        :return: The read_buckets_per_sec of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._read_buckets_per_sec

    @read_buckets_per_sec.setter
    def read_buckets_per_sec(self, read_buckets_per_sec):
        """Sets the read_buckets_per_sec of this BucketS3Performance.

        Read buckets requests processed per second.  # noqa: E501

        :param read_buckets_per_sec: The read_buckets_per_sec of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if read_buckets_per_sec is not None and read_buckets_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `read_buckets_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._read_buckets_per_sec = read_buckets_per_sec

    @property
    def read_objects_per_sec(self):
        """Gets the read_objects_per_sec of this BucketS3Performance.  # noqa: E501

        Read object requests processed per second.  # noqa: E501

        :return: The read_objects_per_sec of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._read_objects_per_sec

    @read_objects_per_sec.setter
    def read_objects_per_sec(self, read_objects_per_sec):
        """Sets the read_objects_per_sec of this BucketS3Performance.

        Read object requests processed per second.  # noqa: E501

        :param read_objects_per_sec: The read_objects_per_sec of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if read_objects_per_sec is not None and read_objects_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `read_objects_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._read_objects_per_sec = read_objects_per_sec

    @property
    def write_buckets_per_sec(self):
        """Gets the write_buckets_per_sec of this BucketS3Performance.  # noqa: E501

        Write buckets requests processed per second.  # noqa: E501

        :return: The write_buckets_per_sec of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._write_buckets_per_sec

    @write_buckets_per_sec.setter
    def write_buckets_per_sec(self, write_buckets_per_sec):
        """Sets the write_buckets_per_sec of this BucketS3Performance.

        Write buckets requests processed per second.  # noqa: E501

        :param write_buckets_per_sec: The write_buckets_per_sec of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if write_buckets_per_sec is not None and write_buckets_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `write_buckets_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._write_buckets_per_sec = write_buckets_per_sec

    @property
    def write_objects_per_sec(self):
        """Gets the write_objects_per_sec of this BucketS3Performance.  # noqa: E501

        Write object requests processed per second.  # noqa: E501

        :return: The write_objects_per_sec of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._write_objects_per_sec

    @write_objects_per_sec.setter
    def write_objects_per_sec(self, write_objects_per_sec):
        """Sets the write_objects_per_sec of this BucketS3Performance.

        Write object requests processed per second.  # noqa: E501

        :param write_objects_per_sec: The write_objects_per_sec of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if write_objects_per_sec is not None and write_objects_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `write_objects_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._write_objects_per_sec = write_objects_per_sec

    @property
    def time(self):
        """Gets the time of this BucketS3Performance.  # noqa: E501

        Sample time in milliseconds since UNIX epoch.  # noqa: E501

        :return: The time of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this BucketS3Performance.

        Sample time in milliseconds since UNIX epoch.  # noqa: E501

        :param time: The time of this BucketS3Performance.  # noqa: E501
        :type: int
        """

        self._time = time

    @property
    def usec_per_other_op(self):
        """Gets the usec_per_other_op of this BucketS3Performance.  # noqa: E501

        Average time, measured in microseconds, it takes the array to process other operations.  # noqa: E501

        :return: The usec_per_other_op of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._usec_per_other_op

    @usec_per_other_op.setter
    def usec_per_other_op(self, usec_per_other_op):
        """Sets the usec_per_other_op of this BucketS3Performance.

        Average time, measured in microseconds, it takes the array to process other operations.  # noqa: E501

        :param usec_per_other_op: The usec_per_other_op of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if usec_per_other_op is not None and usec_per_other_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `usec_per_other_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._usec_per_other_op = usec_per_other_op

    @property
    def usec_per_read_bucket_op(self):
        """Gets the usec_per_read_bucket_op of this BucketS3Performance.  # noqa: E501

        Average time, measured in microseconds, it takes the array to process a read bucket request.  # noqa: E501

        :return: The usec_per_read_bucket_op of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._usec_per_read_bucket_op

    @usec_per_read_bucket_op.setter
    def usec_per_read_bucket_op(self, usec_per_read_bucket_op):
        """Sets the usec_per_read_bucket_op of this BucketS3Performance.

        Average time, measured in microseconds, it takes the array to process a read bucket request.  # noqa: E501

        :param usec_per_read_bucket_op: The usec_per_read_bucket_op of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if usec_per_read_bucket_op is not None and usec_per_read_bucket_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `usec_per_read_bucket_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._usec_per_read_bucket_op = usec_per_read_bucket_op

    @property
    def usec_per_read_object_op(self):
        """Gets the usec_per_read_object_op of this BucketS3Performance.  # noqa: E501

        Average time, measured in microseconds, it takes the array to process a read object request.  # noqa: E501

        :return: The usec_per_read_object_op of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._usec_per_read_object_op

    @usec_per_read_object_op.setter
    def usec_per_read_object_op(self, usec_per_read_object_op):
        """Sets the usec_per_read_object_op of this BucketS3Performance.

        Average time, measured in microseconds, it takes the array to process a read object request.  # noqa: E501

        :param usec_per_read_object_op: The usec_per_read_object_op of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if usec_per_read_object_op is not None and usec_per_read_object_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `usec_per_read_object_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._usec_per_read_object_op = usec_per_read_object_op

    @property
    def usec_per_write_bucket_op(self):
        """Gets the usec_per_write_bucket_op of this BucketS3Performance.  # noqa: E501

        Average time, measured in microseconds, it takes the array to process a write bucket request.  # noqa: E501

        :return: The usec_per_write_bucket_op of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._usec_per_write_bucket_op

    @usec_per_write_bucket_op.setter
    def usec_per_write_bucket_op(self, usec_per_write_bucket_op):
        """Sets the usec_per_write_bucket_op of this BucketS3Performance.

        Average time, measured in microseconds, it takes the array to process a write bucket request.  # noqa: E501

        :param usec_per_write_bucket_op: The usec_per_write_bucket_op of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if usec_per_write_bucket_op is not None and usec_per_write_bucket_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `usec_per_write_bucket_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._usec_per_write_bucket_op = usec_per_write_bucket_op

    @property
    def usec_per_write_object_op(self):
        """Gets the usec_per_write_object_op of this BucketS3Performance.  # noqa: E501

        Average time, measured in microseconds, it takes the array to process a write object request.  # noqa: E501

        :return: The usec_per_write_object_op of this BucketS3Performance.  # noqa: E501
        :rtype: int
        """
        return self._usec_per_write_object_op

    @usec_per_write_object_op.setter
    def usec_per_write_object_op(self, usec_per_write_object_op):
        """Sets the usec_per_write_object_op of this BucketS3Performance.

        Average time, measured in microseconds, it takes the array to process a write object request.  # noqa: E501

        :param usec_per_write_object_op: The usec_per_write_object_op of this BucketS3Performance.  # noqa: E501
        :type: int
        """
        if usec_per_write_object_op is not None and usec_per_write_object_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `usec_per_write_object_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._usec_per_write_object_op = usec_per_write_object_op

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
        if issubclass(BucketS3Performance, dict):
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
        if not isinstance(other, BucketS3Performance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
