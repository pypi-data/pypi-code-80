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

import json
import urllib.request
from argparse import ArgumentParser, Namespace
from gitee_utils.helper import GiteeConfig


def add_arguments(parser: ArgumentParser):
    parser.add_argument('--description', help='short description', metavar='DESC', default=None)
    parser.add_argument('--homepage', help='url with more information', metavar='URL', default=None)
    parser.add_argument('--has-issues', action='store_true', help='has issues', default=True)
    parser.add_argument('--has-wiki', action='store_true', help='has wiki', default=True)
    parser.add_argument('--can-comment', action='store_true', help='can make comments', default=True)
    parser.add_argument('--auto-init', action='store_true', help='create initial commit', default=False)
    parser.add_argument('--gitignore-template', help='apply .gitignore template', metavar='LANG', default=None)
    parser.add_argument('--license-template', help='apply license template', metavar='LICENSE', default=None)
    parser.add_argument('--path', help='path of repository', metavar='PATH', default=None)
    parser.add_argument('--private', action='store_true', help='private repository or not', default=True)
    parser.add_argument('name', help='name of repository')


def execute(config: GiteeConfig, args: Namespace):
    req = urllib.request.Request(
        url='https://gitee.com/api/v5/user/repos',
        method='POST',
        headers={
            'Content-Type': 'application/json;charset=UTF-8'
        },
        data=bytes(json.dumps({
            'access_token': config.access_token,
            'name': args.name,
            'description': args.description,
            'homepage': args.homepage,
            'has_issues': args.has_issues,
            'has_wiki': args.has_wiki,
            'can_comment': args.can_comment,
            'auto_init': args.auto_init,
            'gitignore_template': args.gitignore_template,
            'license_template': args.license_template,
            'path': args.path,
            'private': args.private
        }).encode('utf-8'))
    )

    urllib.request.urlopen(req)
    return 0
