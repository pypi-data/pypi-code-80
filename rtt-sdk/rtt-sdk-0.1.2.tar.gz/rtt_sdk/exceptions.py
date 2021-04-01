# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 NetSPI <rtt.support@netspi.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import functools
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from rtt_sdk.models import TaskErrorInfo


class RTTError(Exception):
    def __init__(
        self,
        message: Union[str, bytes] = "",
        response_code: Optional[int] = None,
        response_body: Union[str, bytes] = None,
    ):
        super().__init__(self, message)
        self.response_code = response_code
        if isinstance(response_body, bytes):
            self.response_body = response_body.decode()
        else:
            self.response_body = response_body
        if isinstance(message, bytes):
            self.message = message.decode()
        else:
            self.message = message

    def __str__(self):
        if self.response_code is not None:
            return f"{self.response_code}: {self.response_body}"
        else:
            return self.message


class RTTTaskError(Exception):
    def __init__(
        self,
        error_info: "TaskErrorInfo",
    ):
        super().__init__(self, error_info.description)
        self.code = error_info.code
        self.description = error_info.description
        self.os_code = error_info.os_code
        self.os_description = error_info.os_description

    def __str__(self):
        parts = [
            self.description,
            f"[{self.code}]" if self.code else None,
            "/" if self.description and self.os_description else None,
            self.os_description,
            f"[{self.os_code}]" if self.os_code else None,
        ]
        return " ".join([p for p in parts if p])


class RTTHttpError(RTTError):
    pass


class RTTServerError(RTTError):
    pass


class RTTIncompatibleServer(RTTServerError):
    pass


class RTTAuthenticationTimedOut(RTTError):
    pass


class RTTAuthenticationError(RTTHttpError):
    pass


class RTTParsingError(RTTHttpError):
    pass


class RTTValidationError(RTTHttpError):
    pass


def on_http_error(error):
    def wrap(f):
        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except RTTHttpError as e:
                raise error(e.message, e.response_code, e.response_body) from e

        return wrapped_f

    return wrap
