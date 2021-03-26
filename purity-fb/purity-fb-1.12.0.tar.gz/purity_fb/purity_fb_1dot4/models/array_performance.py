# coding: utf-8

"""
    Pure Storage FlashBlade REST 1.4 Python SDK

    Pure Storage FlashBlade REST 1.4 Python SDK, developed by [Pure Storage, Inc](http://www.purestorage.com/). Documentations can be found at [purity-fb.readthedocs.io](http://purity-fb.readthedocs.io/).

    OpenAPI spec version: 1.4
    Contact: info@purestorage.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class ArrayPerformance(object):
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
        'name': 'str',
        'bytes_per_op': 'int',
        'bytes_per_read': 'int',
        'bytes_per_write': 'int',
        'others_per_sec': 'int',
        'read_bytes_per_sec': 'int',
        'reads_per_sec': 'int',
        'time': 'int',
        'usec_per_other_op': 'int',
        'usec_per_read_op': 'int',
        'usec_per_write_op': 'int',
        'write_bytes_per_sec': 'int',
        'writes_per_sec': 'int',
        'output_per_sec': 'int',
        'input_per_sec': 'int'
    }

    attribute_map = {
        'name': 'name',
        'bytes_per_op': 'bytes_per_op',
        'bytes_per_read': 'bytes_per_read',
        'bytes_per_write': 'bytes_per_write',
        'others_per_sec': 'others_per_sec',
        'read_bytes_per_sec': 'read_bytes_per_sec',
        'reads_per_sec': 'reads_per_sec',
        'time': 'time',
        'usec_per_other_op': 'usec_per_other_op',
        'usec_per_read_op': 'usec_per_read_op',
        'usec_per_write_op': 'usec_per_write_op',
        'write_bytes_per_sec': 'write_bytes_per_sec',
        'writes_per_sec': 'writes_per_sec',
        'output_per_sec': 'output_per_sec',
        'input_per_sec': 'input_per_sec'
    }

    def __init__(self, name=None, bytes_per_op=None, bytes_per_read=None, bytes_per_write=None, others_per_sec=None, read_bytes_per_sec=None, reads_per_sec=None, time=None, usec_per_other_op=None, usec_per_read_op=None, usec_per_write_op=None, write_bytes_per_sec=None, writes_per_sec=None, output_per_sec=None, input_per_sec=None):  # noqa: E501
        """ArrayPerformance - a model defined in Swagger"""  # noqa: E501

        self._name = None
        self._bytes_per_op = None
        self._bytes_per_read = None
        self._bytes_per_write = None
        self._others_per_sec = None
        self._read_bytes_per_sec = None
        self._reads_per_sec = None
        self._time = None
        self._usec_per_other_op = None
        self._usec_per_read_op = None
        self._usec_per_write_op = None
        self._write_bytes_per_sec = None
        self._writes_per_sec = None
        self._output_per_sec = None
        self._input_per_sec = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if bytes_per_op is not None:
            self.bytes_per_op = bytes_per_op
        if bytes_per_read is not None:
            self.bytes_per_read = bytes_per_read
        if bytes_per_write is not None:
            self.bytes_per_write = bytes_per_write
        if others_per_sec is not None:
            self.others_per_sec = others_per_sec
        if read_bytes_per_sec is not None:
            self.read_bytes_per_sec = read_bytes_per_sec
        if reads_per_sec is not None:
            self.reads_per_sec = reads_per_sec
        if time is not None:
            self.time = time
        if usec_per_other_op is not None:
            self.usec_per_other_op = usec_per_other_op
        if usec_per_read_op is not None:
            self.usec_per_read_op = usec_per_read_op
        if usec_per_write_op is not None:
            self.usec_per_write_op = usec_per_write_op
        if write_bytes_per_sec is not None:
            self.write_bytes_per_sec = write_bytes_per_sec
        if writes_per_sec is not None:
            self.writes_per_sec = writes_per_sec
        if output_per_sec is not None:
            self.output_per_sec = output_per_sec
        if input_per_sec is not None:
            self.input_per_sec = input_per_sec

    @property
    def name(self):
        """Gets the name of this ArrayPerformance.  # noqa: E501

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :return: The name of this ArrayPerformance.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ArrayPerformance.

        The name of the object (e.g., a file system or snapshot)  # noqa: E501

        :param name: The name of this ArrayPerformance.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def bytes_per_op(self):
        """Gets the bytes_per_op of this ArrayPerformance.  # noqa: E501

        Average operation size (read bytes+write bytes/(read ops+write ops))  # noqa: E501

        :return: The bytes_per_op of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._bytes_per_op

    @bytes_per_op.setter
    def bytes_per_op(self, bytes_per_op):
        """Sets the bytes_per_op of this ArrayPerformance.

        Average operation size (read bytes+write bytes/(read ops+write ops))  # noqa: E501

        :param bytes_per_op: The bytes_per_op of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if bytes_per_op is not None and bytes_per_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `bytes_per_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._bytes_per_op = bytes_per_op

    @property
    def bytes_per_read(self):
        """Gets the bytes_per_read of this ArrayPerformance.  # noqa: E501

        Average read size in bytes per read operation  # noqa: E501

        :return: The bytes_per_read of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._bytes_per_read

    @bytes_per_read.setter
    def bytes_per_read(self, bytes_per_read):
        """Sets the bytes_per_read of this ArrayPerformance.

        Average read size in bytes per read operation  # noqa: E501

        :param bytes_per_read: The bytes_per_read of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if bytes_per_read is not None and bytes_per_read < 0:  # noqa: E501
            raise ValueError("Invalid value for `bytes_per_read`, must be a value greater than or equal to `0`")  # noqa: E501

        self._bytes_per_read = bytes_per_read

    @property
    def bytes_per_write(self):
        """Gets the bytes_per_write of this ArrayPerformance.  # noqa: E501

        Average write size in bytes per write operation  # noqa: E501

        :return: The bytes_per_write of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._bytes_per_write

    @bytes_per_write.setter
    def bytes_per_write(self, bytes_per_write):
        """Sets the bytes_per_write of this ArrayPerformance.

        Average write size in bytes per write operation  # noqa: E501

        :param bytes_per_write: The bytes_per_write of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if bytes_per_write is not None and bytes_per_write < 0:  # noqa: E501
            raise ValueError("Invalid value for `bytes_per_write`, must be a value greater than or equal to `0`")  # noqa: E501

        self._bytes_per_write = bytes_per_write

    @property
    def others_per_sec(self):
        """Gets the others_per_sec of this ArrayPerformance.  # noqa: E501

        Other operations processed per second  # noqa: E501

        :return: The others_per_sec of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._others_per_sec

    @others_per_sec.setter
    def others_per_sec(self, others_per_sec):
        """Sets the others_per_sec of this ArrayPerformance.

        Other operations processed per second  # noqa: E501

        :param others_per_sec: The others_per_sec of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if others_per_sec is not None and others_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `others_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._others_per_sec = others_per_sec

    @property
    def read_bytes_per_sec(self):
        """Gets the read_bytes_per_sec of this ArrayPerformance.  # noqa: E501

        Bytes read per second  # noqa: E501

        :return: The read_bytes_per_sec of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._read_bytes_per_sec

    @read_bytes_per_sec.setter
    def read_bytes_per_sec(self, read_bytes_per_sec):
        """Sets the read_bytes_per_sec of this ArrayPerformance.

        Bytes read per second  # noqa: E501

        :param read_bytes_per_sec: The read_bytes_per_sec of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if read_bytes_per_sec is not None and read_bytes_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `read_bytes_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._read_bytes_per_sec = read_bytes_per_sec

    @property
    def reads_per_sec(self):
        """Gets the reads_per_sec of this ArrayPerformance.  # noqa: E501

        Read requests processed per second  # noqa: E501

        :return: The reads_per_sec of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._reads_per_sec

    @reads_per_sec.setter
    def reads_per_sec(self, reads_per_sec):
        """Sets the reads_per_sec of this ArrayPerformance.

        Read requests processed per second  # noqa: E501

        :param reads_per_sec: The reads_per_sec of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if reads_per_sec is not None and reads_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `reads_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._reads_per_sec = reads_per_sec

    @property
    def time(self):
        """Gets the time of this ArrayPerformance.  # noqa: E501

        Sample time in milliseconds since UNIX epoch  # noqa: E501

        :return: The time of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this ArrayPerformance.

        Sample time in milliseconds since UNIX epoch  # noqa: E501

        :param time: The time of this ArrayPerformance.  # noqa: E501
        :type: int
        """

        self._time = time

    @property
    def usec_per_other_op(self):
        """Gets the usec_per_other_op of this ArrayPerformance.  # noqa: E501

        Average time, measured in microseconds, that the array takes to process other operations  # noqa: E501

        :return: The usec_per_other_op of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._usec_per_other_op

    @usec_per_other_op.setter
    def usec_per_other_op(self, usec_per_other_op):
        """Sets the usec_per_other_op of this ArrayPerformance.

        Average time, measured in microseconds, that the array takes to process other operations  # noqa: E501

        :param usec_per_other_op: The usec_per_other_op of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if usec_per_other_op is not None and usec_per_other_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `usec_per_other_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._usec_per_other_op = usec_per_other_op

    @property
    def usec_per_read_op(self):
        """Gets the usec_per_read_op of this ArrayPerformance.  # noqa: E501

        Average time, measured in microseconds, that the array takes to process a read request  # noqa: E501

        :return: The usec_per_read_op of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._usec_per_read_op

    @usec_per_read_op.setter
    def usec_per_read_op(self, usec_per_read_op):
        """Sets the usec_per_read_op of this ArrayPerformance.

        Average time, measured in microseconds, that the array takes to process a read request  # noqa: E501

        :param usec_per_read_op: The usec_per_read_op of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if usec_per_read_op is not None and usec_per_read_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `usec_per_read_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._usec_per_read_op = usec_per_read_op

    @property
    def usec_per_write_op(self):
        """Gets the usec_per_write_op of this ArrayPerformance.  # noqa: E501

        Average time, measured in microseconds, that the array takes to process a write request  # noqa: E501

        :return: The usec_per_write_op of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._usec_per_write_op

    @usec_per_write_op.setter
    def usec_per_write_op(self, usec_per_write_op):
        """Sets the usec_per_write_op of this ArrayPerformance.

        Average time, measured in microseconds, that the array takes to process a write request  # noqa: E501

        :param usec_per_write_op: The usec_per_write_op of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if usec_per_write_op is not None and usec_per_write_op < 0:  # noqa: E501
            raise ValueError("Invalid value for `usec_per_write_op`, must be a value greater than or equal to `0`")  # noqa: E501

        self._usec_per_write_op = usec_per_write_op

    @property
    def write_bytes_per_sec(self):
        """Gets the write_bytes_per_sec of this ArrayPerformance.  # noqa: E501

        Bytes written per second  # noqa: E501

        :return: The write_bytes_per_sec of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._write_bytes_per_sec

    @write_bytes_per_sec.setter
    def write_bytes_per_sec(self, write_bytes_per_sec):
        """Sets the write_bytes_per_sec of this ArrayPerformance.

        Bytes written per second  # noqa: E501

        :param write_bytes_per_sec: The write_bytes_per_sec of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if write_bytes_per_sec is not None and write_bytes_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `write_bytes_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._write_bytes_per_sec = write_bytes_per_sec

    @property
    def writes_per_sec(self):
        """Gets the writes_per_sec of this ArrayPerformance.  # noqa: E501

        Write requests processed per second  # noqa: E501

        :return: The writes_per_sec of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._writes_per_sec

    @writes_per_sec.setter
    def writes_per_sec(self, writes_per_sec):
        """Sets the writes_per_sec of this ArrayPerformance.

        Write requests processed per second  # noqa: E501

        :param writes_per_sec: The writes_per_sec of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if writes_per_sec is not None and writes_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `writes_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._writes_per_sec = writes_per_sec

    @property
    def output_per_sec(self):
        """Gets the output_per_sec of this ArrayPerformance.  # noqa: E501

        Bytes read per second  # noqa: E501

        :return: The output_per_sec of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._output_per_sec

    @output_per_sec.setter
    def output_per_sec(self, output_per_sec):
        """Sets the output_per_sec of this ArrayPerformance.

        Bytes read per second  # noqa: E501

        :param output_per_sec: The output_per_sec of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if output_per_sec is not None and output_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `output_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._output_per_sec = output_per_sec

    @property
    def input_per_sec(self):
        """Gets the input_per_sec of this ArrayPerformance.  # noqa: E501

        Bytes written per second  # noqa: E501

        :return: The input_per_sec of this ArrayPerformance.  # noqa: E501
        :rtype: int
        """
        return self._input_per_sec

    @input_per_sec.setter
    def input_per_sec(self, input_per_sec):
        """Sets the input_per_sec of this ArrayPerformance.

        Bytes written per second  # noqa: E501

        :param input_per_sec: The input_per_sec of this ArrayPerformance.  # noqa: E501
        :type: int
        """
        if input_per_sec is not None and input_per_sec < 0:  # noqa: E501
            raise ValueError("Invalid value for `input_per_sec`, must be a value greater than or equal to `0`")  # noqa: E501

        self._input_per_sec = input_per_sec

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
        if issubclass(ArrayPerformance, dict):
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
        if not isinstance(other, ArrayPerformance):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
