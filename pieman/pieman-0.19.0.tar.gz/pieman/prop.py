# Copyright (C) 2017-2021 Evgeny Golyshev <eugulixes@gmail.com>
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

"""Module intended to simplify working with pieman.yml files. """

import yaml


TYPES_SCHEME = {
    'repos': (list, ),
    'codename': (str, ),
    'base': (list, str),
    'includes': (list, str),
    'boot': (list, str),
    'params': (list, ),
    'kernel': {
        'package': (str, ),
        'rebuild': (bool, ),
        'patches': (str, ),
    },
}


class PropDoesNotExist(Exception):
    """Exception raised when attempting to get a property which does not
    exist. """
    def __init__(self, par_name, cur_name):
        message = ('{} does not have property {}'.format(par_name, cur_name))
        Exception.__init__(self, message)


class RootDoesNotExist(Exception):
    """Exception raised when attempting to get the root which does not
    exist. """


class UnknownProp(Exception):
    """Exception raised when attempting to get a property which may exist
    but is not mentioned in the specification. """


class UnprintableType(Exception):
    """Exception raised when attempting to print a property the type of which
    is neither str nor list. """


class Prop:  # pylint: disable=too-few-public-methods
    """Class representing a single property. """

    def __init__(self, prop, prop_type):
        self.prop, self._prop_type = prop, prop_type

    def echo(self):
        """Writes a property value to stdout or raises
        `UnprintableType` if the property type is neither str nor list.
        """
        if list in self._prop_type or str in self._prop_type:
            if isinstance(self.prop, str):
                self.prop = [self.prop]

            for line in self.prop:
                print(line)
        else:
            raise UnprintableType


class PropsList:  # pylint: disable=too-few-public-methods
    """Class implementing the interface for working with pieman.yml files. """

    def __init__(self, infile):
        with open(infile, 'r') as infile:
            self._props = yaml.load(infile, Loader=yaml.FullLoader)

    def get_prop(self, props_chain):
        """Gets a property value. To get the value the full path to
        the property must be specified starting with the root.
        """

        if props_chain:
            par_name = props_chain[0]
            try:
                cur_prop = self._props[par_name]
            except KeyError as exc:
                raise RootDoesNotExist from exc

            cur_type = TYPES_SCHEME

            for prop_name in props_chain[1:]:
                try:
                    cur_prop = cur_prop[prop_name]
                except KeyError as exc:
                    raise PropDoesNotExist(par_name, prop_name) from exc

                try:
                    cur_type = cur_type[prop_name]
                except KeyError as exc:
                    raise UnknownProp from exc

                par_name = prop_name

            if isinstance(cur_type, dict):
                cur_type = (dict, )

            return Prop(cur_prop, cur_type)

        return None
