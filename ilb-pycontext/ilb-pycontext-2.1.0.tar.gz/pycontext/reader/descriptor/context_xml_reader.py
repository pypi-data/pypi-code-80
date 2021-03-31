#  Copyright (c) 2020 Bystrobank
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import getpass
import xml.etree.ElementTree as tree
from pathlib import Path
from sys import platform
from typing import List, Any

from pycontext import ContextVariable
from pycontext.reader.reader import ContextReader
from pycontext.tool.typeparser import TypeParser, JavaTypeParser
from . import MalformedSourceError


class ContextXmlReader(ContextReader):
    """ Reader of context.xml file, extracts <Environment/> element/s to the context variable/s. """

    def __init__(
        self,
        appname: str = None,
        produced_ttl: float = None,
        type_parser: TypeParser = JavaTypeParser(),
    ) -> None:
        """
        Generic constructor.
        :param appname: application name, used for looking for related context.xml file
        :param type_parser: parser for cast element's value to Python type using element type
        :param produced_ttl: unique produced reader.descriptor element time to life
        """
        self._file_path: Path = self._default_path(appname)
        self._type_parser = type_parser
        self._produced_ttl = produced_ttl

    def read_all(self) -> List[ContextVariable]:
        """
        Reads context.xml reader.descriptor elements as list of context variables.
        :raises ValueError when element doesn't contains 'name', 'type', or 'value' attributes
        :return: context variables list
        """
        variables: List[ContextVariable] = []
        root: tree.Element = self._get_descriptor_root()
        for elem in root.findall("./Environment"):
            for attr in ["name", "type", "value"]:
                if attr not in elem.attrib:
                    raise ValueError(f"'{attr}' attribute not found in {elem}")
            variables.append(self._parse_env(elem))
        return variables

    def read(self, key: str) -> ContextVariable:
        """
        Reads context.xml reader.descriptor element as context variable by key.
        :param key: element name
        :return: context variable
        """
        root: tree.Element = self._get_descriptor_root()
        elem = root.find(f".//Environment/[@name='{key}']")
        if elem is not None:
            return self._parse_env(elem)
        raise ValueError(f"'{key}' value not found in {self._file_path}")

    def _get_descriptor_root(self):
        """
        Extracts root reader.descriptor element for lookup.
        :return: reader.descriptor root element
        """
        try:
            return tree.parse(self._file_path).getroot()
        except tree.ParseError as e:
            raise MalformedSourceError(self._file_path, str(e))

    def _parse_env(self, element: Any) -> ContextVariable:
        """
        Parses <Environment/> element to context variable.
        :param element: element to parse
        :return: context variable
        """
        return ContextVariable(
            name=element.attrib["name"],
            source=self,
            value=self._type_parser.to_type(element.attrib["value"], element.attrib["type"]),
            locked=element.attrib.get("override") == "true",
            expires=self._produced_ttl,
        )

    def __str__(self):
        return f"{type(self).__module__}.{type(self).__name__}[{self._file_path}]"

    @staticmethod
    def _default_path(appname):
        """
        Default 'context.xml' file path depending on the platform.
        :return: file path
        """
        if platform.startswith("linux") or platform == "darwin":
            default_path = Path.home().joinpath(".config/context.xml")
            if not default_path.is_file():
                default_path = Path(f"/etc/python/{getpass.getuser()}/{appname or 'context'}.xml")
            return default_path
        elif platform.startswith("win"):
            return Path.home().joinpath("context.xml")
