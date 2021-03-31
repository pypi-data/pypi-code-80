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

import re
from pathlib import Path
from sys import platform
from typing import Any

import ldap

from pycontext.resolver.resolver import ResourceResolver


class LdapResolver(ResourceResolver):
    """
    LDAP resolver for reference values.
    """

    def __init__(self, uri: str, base: str, prefix: str = None) -> None:
        """
        Generic constructor.
        :param uri: LDAP URI
        :param base: LDAP base group
        :param prefix: LDAP prefix
        """
        self._uri = uri
        self._base = base
        self._prefix = prefix

    @staticmethod
    def from_ldap_conf() -> "LdapResolver":
        """
        Initializes instance by 'ldap.conf' file by extracting BASE and URI from it
        :return: ldap resolver
        """

        def _ldap_conf_path() -> Path:
            """
            Default 'ldap.conf' file path, depending on the platform.
            :return: file path
            """
            if platform.startswith("linux"):
                return Path("/etc/openldap/ldap.conf")
            elif platform == "darwin":
                return Path("/private/etc/openldap/ldap.conf")
            elif platform.startswith("win"):
                return Path("C:/OpenLDAP/ldap.conf")

        try:
            with _ldap_conf_path().open() as conf:
                uri, base = None, None
                for line in conf:
                    base = re.search("^BASE (.*)$", line.strip()) if base is None else base
                    uri = re.search("^URI (.*)$", line.strip()) if uri is None else uri
            if uri is None or base is None:
                raise ValueError(f"LDAP config file doesn't contains needed attributes: {_ldap_conf_path()}")
            return LdapResolver(uri=uri.group(1).strip(), base=base.group(1).strip())
        finally:
            conf.close()

    def resolve(self, key: str) -> Any:
        """
        Resolves context variable value by it's key.
        :param key: variable key to resolve
        :return: variable value
        """
        cn = self._build_common_name(key)
        return self._search_by_common_name(cn)

    def _build_common_name(self, key: str) -> str:
        """
        Builds LDAP common name from key.
        If specified without prefix (.blah.blah.variable), prefix will be added from specified prefix in constructor.
        :param key: variable key to resolve
        :raises ValueError when prefix is not set, and key specified without prefix
        :return: variable value
        """
        if key[0] == "." and self._prefix is None:
            raise ValueError(f"LDAP prefix is not set, key to resolve doesn't contain prefix too: {key}")
        return self._prefix + key if key[0] == "." else key

    def _search_by_common_name(self, common_name: str) -> str:
        """
        Initializes LDAP service and searches variable by common name (CN).
        :param common_name: search query parameter
        :raises ValueError when resource or resource's value not found
        :return: variable
        """
        ldap_service = ldap.initialize(self._uri)
        resource = ldap_service.search_s(
            self._base,
            ldap.SCOPE_SUBTREE,
            f"(&(objectClass=labeledURIObject)(cn={common_name}))",
            ["dn", "labeleduri"],
        )

        if len(resource) == 0:
            raise ValueError(f"LDAP resource not found: '{common_name}'")

        for _, entry in resource:
            if len(entry["labeledURI"]) > 0:
                return entry["labeledURI"][0].decode("utf-8")
            else:
                raise ValueError(f"LDAP resource value not found: '{common_name}'")

    def __str__(self):
        return f"{type(self).__module__}.{type(self).__name__}[{self._uri}]"
