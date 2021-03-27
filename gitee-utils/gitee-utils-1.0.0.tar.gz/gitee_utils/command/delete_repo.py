# -*- coding: utf-8 -*-
# Copyright (C) 2020 HE Yaowen <he.yaowen@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import urllib.request
import urllib.parse
from argparse import ArgumentParser, Namespace
from gitee_utils.helper import GiteeConfig


def add_arguments(parser: ArgumentParser):
    parser.add_argument('--owner', help='repository owner', metavar='OWNER')
    parser.add_argument('name', help='name of repository')


def execute(config: GiteeConfig, args: Namespace):
    req = urllib.request.Request(
        url='https://gitee.com/api/v5/repos/%s/%s?%s' % (args.owner, args.name, urllib.parse.urlencode({'access_token': config.access_token})),
        method='DELETE',
        headers={
            'Content-Type': 'application/json;charset=UTF-8'
        })

    urllib.request.urlopen(req)
