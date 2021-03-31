# Copyright (c) 2018 Gareth Dunstone <gareth.dunstone@anu.edu.au>
# Copyright (c) 2019-2021 Gekkonid Consulting/Kevin Murray <foss@kdmurray.id.au>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .base import PipelineStep


def truncate_nth_minute(datetime, nth_minute):
    """
    Truncates the datetime to the *nth* minute closest to it.
    For instance, with ``nth_minute=5`` it truncates to the nearest whole five minute interval.

    :param datetime: an initialized datetime object
    :type datetime: :class:`datetime`
    :param nth_minute: the minute to truncate to
    :type nth_minute: int
    :return: truncated datetime
    :rtype: :class:`datetime` object
    """
    if not 0 <= nth_minute < 60:
        raise ValueError(
            '`nth_minute` must be >= 0 and < 60, was {0}'.format(nth_minute)
        )

    for m in range(0, 60, nth_minute):
        if m <= datetime.minute < m + nth_minute:
            return datetime.replace(minute=m, second=0, microsecond=0)


def truncate_nth_hour(datetime, nth_hour):
    """
    Truncates the datetime to the *nth* hour closest to it.
    For instance, with ``nth_hour=2`` it truncates to the nearest whole two hour interval.

    :param datetime: an initialized datetime object
    :type datetime: :class:`datetime`
    :param nth_hour: the minute to truncate to
    :type nth_hour: int
    :return: truncated datetime
    :rtype: :class:`datetime` object
    """
    if not 0 <= nth_hour < 24:
        raise ValueError(
            '`nth_hour` must be >= 0 and < 60, was {0}'.format(nth_hour)
        )

    for m in range(0, 24, nth_hour):
        if m <= datetime.hour < m + nth_hour:
            return datetime.replace(hour=m, minute=0, second=0, microsecond=0)


class TruncateTimeStep(PipelineStep):
    """
    Truncates datetime of a TimestreamFile, usually to provide consistent
    interval measurements given slight time differences in recording hardware.
    """

    def __init__(self, truncate_to=10):
        """
        :param truncate_to: Minutes to truncate to (between 0-60)
        :type truncate_to: int
        """
        self.truncate_to = int(truncate_to)

    def process_file(self, file):
        file.instant.datetime = truncate_nth_minute(file.instant.datetime, self.truncate_to)
        return file
