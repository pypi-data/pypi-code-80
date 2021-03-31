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

from pathlib import Path
from typing import List, Any
from xml.etree import ElementTree as Tree
from xml.etree.ElementTree import ParseError, Element

from pycontext import ContextVariable
from pycontext.reader.reader import ContextReader
from pycontext.resolver import ResourceResolver
from pycontext.tool.typeparser import TypeParser, JavaTypeParser
from . import MalformedSourceError


class WebXmlReader(ContextReader):
    """
    Reader of 'web.xml' reader.descriptor, extracts '<resource-env-ref/>'
    and '<env-entry/>' elements to the context variables/s.
    """

    descriptor_ns = "http://java.sun.com/xml/ns/j2ee"

    def __init__(
        self,
        file_path: Path,
        produced_ttl: float = None,
        type_parser: TypeParser = JavaTypeParser(),
        resource_resolvers: List[ResourceResolver] = None,
    ) -> None:
        """
        Generic constructor.
        :param file_path: context.xml file path
        :param produced_ttl: unique produced reader.descriptor element time to life
        :param type_parser: parser for cast element's value to Python type using element type
        :param resource_resolvers: resolvers for reference variables
        """
        self._file_path = file_path
        self._produced_ttl = produced_ttl
        self._type_parser = type_parser
        self._resource_resolvers = resource_resolvers

    def read_all(self) -> List[ContextVariable]:
        """
        Reads '<resource-env-ref/>' and '<env-entry/>' elements to list of context variables.
        :return: list of context variables
        """
        try:
            root: Element = Tree.parse(self._file_path).getroot()
        except ParseError as e:
            raise MalformedSourceError(self._file_path, str(e))

        if not self._is_j2ee_descriptor(root):
            raise ValueError(f'Root tag is not matching j2ee reader.descriptor: "{root.tag}"')

        resource_env_refs = [
            self._parse_resource_env_ref(res)
            for res in root.findall("./j2ee:resource-env-ref", {"j2ee": self.descriptor_ns})
        ]

        env_entries = [
            self._parse_env_entry(entry) for entry in root.findall("./j2ee:env-entry", {"j2ee": self.descriptor_ns})
        ]

        return resource_env_refs + env_entries

    def read(self, key: str) -> "ContextVariable":
        """
        Reads '<resource-env-ref/>' / '<env-entry/>' element to context variable by key.
        :return: context variable
        """
        try:
            root: Element = Tree.parse(self._file_path).getroot()
        except ParseError as e:
            raise MalformedSourceError(self._file_path, str(e))

        elem: Element = root.find(
            f".//j2ee:resource-env-ref[j2ee:resource-env-ref-name='{key}']",
            {"j2ee": self.descriptor_ns},
        )
        if elem is not None:
            try:
                return self._parse_resource_env_ref(elem)
            except ValueError:
                pass

        elem: Element = root.find(
            f".//j2ee:env-entry[j2ee:env-entry-name='{key}']",
            {"j2ee": self.descriptor_ns},
        )

        if elem is not None:
            try:
                return self._parse_env_entry(elem)
            except ValueError:
                pass

        raise ValueError(
            f"'{key}' variable not found in {self._file_path}"
            if self._resource_resolvers is None
            else f"'{key}' variable not found in {self._file_path} "
            f"and by {list(map(str, self._resource_resolvers))}"
        )

    def _is_j2ee_descriptor(self, root: Any) -> bool:
        """
        :param root: root reader.descriptor element.
        :return: is reader.descriptor matching j2ee
        """
        return root.tag == f"{{{self.descriptor_ns}}}web-app"

    def _parse_resource_env_ref(self, element: Any) -> ContextVariable:
        """
        Parses <resource-env-ref/> element to the context variable.
        :param element: element to parse.
        :return: context variable
        """
        name = self._get_element_attribute_checked(element, "resource-env-ref-name")

        if self._resource_resolvers is None:
            raise ValueError(
                f"Can't find variable for resource-env-ref-name element '{name}' without resource resolvers"
            )
        else:
            value = self._get_element_attribute(element, "resource-env-ref-value") or self._lookup_reference_value(name)

        return ContextVariable(
            name=name,
            source=self,
            value=self._type_parser.to_type(
                value,
                self._get_element_attribute_checked(element, "resource-env-ref-type"),
            ),
            expires=self._produced_ttl,
        )

    def _parse_env_entry(self, element: Any) -> ContextVariable:
        """
        Parses <env-entry/> element to context variable.
        :param element: element to parse
        :return: context variable
        """
        name = self._get_element_attribute_checked(element, "env-entry-name")

        if self._resource_resolvers is None:
            value = self._get_element_attribute_checked(element, "env-entry-value")
        else:
            value = self._get_element_attribute(element, "env-entry-value") or self._lookup_reference_value(name)

        return ContextVariable(
            name=name,
            source=self,
            value=self._type_parser.to_type(
                value,
                self._get_element_attribute_checked(element, "env-entry-type"),
            ),
            expires=self._produced_ttl,
        )

    def _get_element_attribute_checked(self, element: Any, attr_name: str) -> Any:
        """
        Gets specified element's attribute.
        :param element: element to get attribute from
        :param attr_name: attribute name
        :raises ValueError if attribute not found
        :return: element attribute value
        """
        attr_value = element.find(f"j2ee:{attr_name}", {"j2ee": self.descriptor_ns})
        if attr_value is None:
            raise ValueError(f"'{attr_name}' attribute not found in {element}")
        else:
            return attr_value.text

    def _get_element_attribute(self, element: Any, attr_name: str) -> Any:
        """
        Gets specified element's attribute.
        :param element: element to get attribute from
        :param attr_name: attribute name
        :return: element attribute value or None
        """
        attr_value = element.find(f"j2ee:{attr_name}", {"j2ee": self.descriptor_ns})
        return attr_value.text if attr_value is not None else None

    def _lookup_reference_value(self, name):
        """
        Lookups reference variable value by name using specified resource resolvers.
        :param name: variable name
        :return: variable value
        """
        for resolver in self._resource_resolvers:
            try:
                return resolver.resolve(name)
            except:
                continue
        raise ValueError(
            f"Can't find value for '{name}' variable resource by "
            f"{list(map(str, self._resource_resolvers))} resolvers"
        )

    def __str__(self):
        return f"{type(self).__module__}.{type(self).__name__}[{self._file_path}]"
