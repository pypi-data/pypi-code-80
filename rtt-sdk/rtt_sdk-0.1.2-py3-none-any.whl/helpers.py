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

import os

from rtt_sdk.models import TaskDelivery, TaskStatus


def get_current_file_name() -> str:
    return os.path.basename(__file__)


def is_task_finished(delivery: TaskDelivery) -> bool:
    return delivery in [TaskDelivery.completed, TaskDelivery.blocked, TaskDelivery.invalid]


def is_task_failed(status: TaskStatus) -> bool:
    return status in [TaskStatus.failure, TaskStatus.warning, TaskStatus.critical]
