#!/usr/bin/env python
#
# License: BSD
#   https://raw.githubusercontent.com/stonier/groot_rocker_extensions/devel/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
Export a coloured, named prompt to ~/.bash_profile on container creation.
"""

##############################################################################
# Imports
##############################################################################

import em
import pkgutil
import os
import pwd
import re
import typing

import groot_rocker

##############################################################################
# Extension
##############################################################################


class NamedPrompt(groot_rocker.extensions.RockerExtension):

    @classmethod
    def get_name(cls) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()  # CamelCase to underscores

    def precondition_environment(self, unused_cli_args: typing.Dict[str, str]):
        pass

    def validate_environment(self, unused_cli_args: typing.Dict[str, str]):
        pass

    def get_preamble(self, unused_cli_args: typing.Dict[str, str]) -> str:
        return ''

    def get_snippet(self, cli_args: typing.Dict[str, str]) -> str:
        snippet = pkgutil.get_data(
            'groot_rocker_extensions',
            'templates/named_prompt.Dockerfile.em'
        ).decode('utf-8')
        substitutions = {}
        userinfo = pwd.getpwuid(os.getuid())
        substitutions['user_name'] = getattr(userinfo, 'pw_' + 'name')
        if 'container_name' in cli_args and cli_args['container_name']:
            substitutions['container_name'] = cli_args['container_name']
        else:
            substitutions['container_name'] = r'\h'
        dockerfile = em.expand(snippet, substitutions)
        return dockerfile

    def get_docker_args(self, unused_cli_args: typing.Dict[str, str]) -> str:
        return ""

    @staticmethod
    def register_arguments(parser, defaults={}):
        # TODO: what to do with the defaults arg?
        parser.add_argument(
            '--named-prompt',
            action='store_true',
            help='export a named prompt via PS1 to ~/.bash_profile'
        )
