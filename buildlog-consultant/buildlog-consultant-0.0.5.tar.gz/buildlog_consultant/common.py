#!/usr/bin/python
# Copyright (C) 2019-2021 Jelmer Vernooij <jelmer@jelmer.uk>
# encoding: utf-8
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

import logging
import os
import posixpath
from typing import List, Optional, Tuple
import re
import textwrap

from . import Problem, SingleLineMatch, problem


logger = logging.getLogger(__name__)


@problem("missing-python-module")
class MissingPythonModule(Problem):

    module: str
    python_version: Optional[str] = None
    minimum_version: Optional[str] = None

    def __str__(self):
        if self.python_version:
            ret = "Missing python %d module: " % self.python_version
        else:
            ret = "Missing python module: "
        ret += self.module
        if self.minimum_version:
            return ret + " (>= %s)" % self.minimum_version
        else:
            return ret

    def __repr__(self):
        return "%s(%r, python_version=%r, minimum_version=%r)" % (
            type(self).__name__,
            self.module,
            self.python_version,
            self.minimum_version,
        )


class MissingPythonDistribution(Problem):

    kind = "missing-python-distribution"

    def __init__(self, distribution, python_version=None, minimum_version=None):
        self.distribution = distribution
        self.python_version = python_version
        self.minimum_version = minimum_version

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and other.distribution == self.distribution
            and other.python_version == self.python_version
            and other.minimum_version == self.minimum_version
        )

    def __str__(self):
        if self.python_version:
            ret = "Missing python %d distribution: " % self.python_version
        else:
            ret = "Missing python distribution: "
        ret += self.distribution
        if self.minimum_version:
            return ret + " (>= %s)" % self.minimum_version
        else:
            return ret

    @classmethod
    def from_requirement_str(cls, text, python_version=None):
        if ">=" in text:
            text, minimum = text.split(">=")
            return cls(text, python_version, minimum)
        return cls(text, python_version)

    def __repr__(self):
        return "%s(%r, python_version=%r, minimum_version=%r)" % (
            type(self).__name__,
            self.distribution,
            self.python_version,
            self.minimum_version,
        )


def python_module_not_found(m):
    try:
        return MissingPythonModule(m.group(2), python_version=None)
    except IndexError:
        return MissingPythonModule(m.group(1), python_version=None)


def python_cmd_module_not_found(m):
    if m.group(1).endswith('python3'):
        python_version = 3
    elif m.group(1).endswith('python2'):
        python_version = 2
    else:
        python_version = None
    return MissingPythonModule(m.group(3), python_version=python_version)


def python_submodule_not_found(m):
    return MissingPythonModule(m.group(2) + '.' + m.group(1), python_version=None)


def python2_module_not_found(m):
    return MissingPythonModule(m.group(1), python_version=2)


def python3_module_not_found(m):
    return MissingPythonModule(m.group(1), python_version=3)


def sphinx_module_not_found(m):
    module = m.group(1).strip("'")
    return MissingPythonModule(module)


def python_reqs_not_found(m):
    expr = m.group(2)
    expr = expr.split(";")[0]
    return MissingPythonDistribution.from_requirement_str(expr)


def python2_reqs_not_found(m):
    expr = m.group(1)
    if ">=" in expr:
        pkg, minimum = expr.split(">=")
        return MissingPythonModule(pkg.strip(), 2, minimum.strip())
    if " " not in expr:
        return MissingPythonModule(expr, 2)
    # Hmm
    return None


def pkg_resources_distribution_not_found(m):
    expr = m.group(1)
    return MissingPythonDistribution.from_requirement_str(expr)


@problem("missing-vague-dependency")
class MissingVagueDependency:

    name: str
    url: Optional[str] = None
    minimum_version: Optional[str] = None

    def __str__(self):
        return "Missing dependency: %s" % self.name


@problem("missing-qt")
class MissingQt:

    def __str__(self):
        return "Missing QT installation"


@problem("missing-x11")
class MissingX11:

    def __str__(self):
        return "Missing X11 headers"


@problem("missing-git-identity")
class MissingGitIdentity:

    def __str__(self):
        return "Missing Git Identity"


@problem("missing-file")
class MissingFile:

    path: str

    def __str__(self):
        return "Missing file: %s" % self.path


def file_not_found(m):
    if m.group(1).startswith("/") and not m.group(1).startswith("/<<PKGBUILDDIR>>"):
        return MissingFile(m.group(1))
    return None


def webpack_file_missing(m):
    path = posixpath.join(m.group(2), m.group(1))
    if path.startswith("/") and not path.startswith("/<<PKGBUILDDIR>>"):
        return MissingFile(path)
    return None


@problem("missing-jdk-file")
class MissingJDKFile:

    jdk_path: str
    filename: str

    def __str__(self):
        return "Missing JDK file %s (JDK Path: %s)" % (self.filename, self.jdk_path)


@problem("missing-jdk")
class MissingJDK:

    jdk_path: str

    def __str__(self):
        return "Missing JDK (JDK Path: %s)" % (self.jdk_path)


@problem("missing-jre")
class MissingJRE:

    def __str__(self):
        return "Missing JRE"


def jdk_file_missing(m):
    return MissingJDKFile(m.group(2), m.group(1))


def jdk_missing(m):
    return MissingJDK(m.group(1))


def jre_missing(m):
    return MissingJRE()


def interpreter_missing(m):
    if m.group(1).startswith("/"):
        if m.group(1).startswith("/<<PKGBUILDDIR>>"):
            return None
        return MissingFile(m.group(1))
    if "/" in m.group(1):
        return None
    return MissingCommand(m.group(1))


@problem("chroot-not-found")
class ChrootNotFound:

    chroot: str

    def __str__(self):
        return "Chroot not found: %s" % self.chroot


@problem("missing-sprockets-file")
class MissingSprocketsFile:

    name: str
    content_type: str

    def __str__(self):
        return "Missing sprockets file: %s (type: %s)" % (self.name, self.content_type)


def sprockets_file_not_found(m):
    return MissingSprocketsFile(m.group(1), m.group(2))


@problem("missing-go-package")
class MissingGoPackage:

    package: str

    def __str__(self):
        return "Missing Go package: %s" % self.package


def missing_go_package(m):
    return MissingGoPackage(m.group(1))


@problem("missing-c-header")
class MissingCHeader:

    header: str

    def __str__(self):
        return "Missing C Header: %s" % self.header


def c_header_missing(m):
    return MissingCHeader(m.group(1))


@problem("missing-node-module")
class MissingNodeModule:

    module: str

    def __str__(self):
        return "Missing Node Module: %s" % self.module


@problem("missing-node-package")
class MissingNodePackage(Problem):

    package: str

    def __str__(self):
        return "Missing Node Package: %s" % self.package


def node_module_missing(m):
    if m.group(1).startswith("/<<PKGBUILDDIR>>/"):
        return None
    if m.group(1).startswith("./"):
        return None
    return MissingNodeModule(m.group(1))


@problem("command-missing")
class MissingCommand:

    command: str

    def __str__(self):
        return "Missing command: %s" % self.command


@problem("no-secret-gpg-key")
class MissingSecretGpgKey:

    def __str__(self):
        return "No secret GPG key is present"


@problem("no-vcversioner-version")
class MissingVcVersionerVersion:

    def __str__(self):
        return "vcversion could not find a git directory or version.txt file"


class MissingConfigure(Problem):

    kind = "missing-configure"

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __str__(self):
        return "Missing configure script"

    def __repr__(self):
        return "%s()" % (type(self).__name__,)


def command_missing(m):
    command = m.group(1)
    if "PKGBUILDDIR" in command:
        return None
    if command == "./configure":
        return MissingConfigure()
    if command.startswith("./") or command.startswith("../"):
        return None
    if command == "debian/rules":
        return None
    return MissingCommand(command)


class MissingJavaScriptRuntime(Problem):

    kind = "javascript-runtime-missing"

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __repr__(self):
        return "%s()" % (type(self).__name__,)

    def __str__(self):
        return "Missing JavaScript Runtime"


def javascript_runtime_missing(m):
    return MissingJavaScriptRuntime()


class MissingPkgConfig(Problem):

    kind = "pkg-config-missing"

    def __init__(self, module, minimum_version=None):
        self.module = module
        self.minimum_version = minimum_version

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.module == other.module
            and self.minimum_version == other.minimum_version
        )

    def __str__(self):
        if self.minimum_version:
            return "Missing pkg-config file: %s (>= %s)" % (
                self.module,
                self.minimum_version,
            )
        else:
            return "Missing pkg-config file: %s" % self.module

    def __repr__(self):
        return "%s(%r, minimum_version=%r)" % (
            type(self).__name__,
            self.module,
            self.minimum_version,
        )


class MissingGoRuntime(Problem):

    kind = 'missing-go-runtime'

    def __repr__(self):
        return "%s()" % (type(self).__name__, )

    def __str__(self):
        return "go runtime is missing"

    def __eq__(self, other):
        return isinstance(self, type(other))


def pkg_config_missing(m):
    expr = m.group(1).strip().split("\t")[0]
    if ">=" in expr:
        pkg, minimum = expr.split(">=", 1)
        return MissingPkgConfig(pkg.strip(), minimum.strip())
    if " " not in expr:
        return MissingPkgConfig(expr)
    # Hmm
    return None


def meson_pkg_config_missing(m):
    return MissingPkgConfig(m.group(3))


def meson_pkg_config_too_low(m):
    return MissingPkgConfig(m.group(3), m.group(4))


def meson_c_library_missing(m):
    return MissingLibrary(m.group(3))


def cmake_pkg_config_missing(m):
    return MissingPkgConfig(m.group(1))


class CMakeFilesMissing(Problem):

    kind = "cmake-files-missing"

    def __init__(self, filenames):
        self.filenames = filenames

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.filenames == other.filenames

    def __str__(self):
        return "Missing CMake package configuration files: %r" % (self.filenames,)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.filenames)


class DhWithOrderIncorrect(Problem):

    kind = "debhelper-argument-order"

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __str__(self):
        return "dh argument order is incorrect"


def dh_with_order(m):
    return DhWithOrderIncorrect()


@problem("no-space-on-device", is_global=True)
class NoSpaceOnDevice:

    def __str__(self):
        return "No space on device"


def install_no_space(m):
    return NoSpaceOnDevice()


@problem("missing-perl-predeclared")
class MissingPerlPredeclared:

    name: str

    def __str__(self):
        return "missing predeclared function: %s" % self.name


@problem("missing-perl-module")
class MissingPerlModule:

    filename: str
    module: str
    inc: Optional[List[str]] = None

    def __str__(self):
        if self.filename or self.inc:
            return "Missing Perl module: %s (filename: %r, inc: %r)" % (
                self.module,
                self.filename,
                self.inc,
            )
        else:
            return "Missing Perl Module: %s" % self.module


def perl_missing_module(m):
    return MissingPerlModule(m.group(1) + ".pm", m.group(2), m.group(3).split(" "))


def perl_expand_failed(m):
    return MissingPerlModule(None, m.group(1).strip().strip("'"), None)


def perl_missing_plugin(m):
    return MissingPerlModule(None, m.group(1), None)


def perl_missing_author_dep(m):
    return MissingPerlModule(None, m.group(1), None)


@problem("missing-perl-file")
class MissingPerlFile:

    filename: str
    inc: Optional[List[str]] = None

    def __str__(self):
        return "Missing Perl file: %s (inc: %r)" % (self.filename, self.inc)


def perl_missing_file(m):
    return MissingPerlFile(m.group(1), m.group(2).split(" "))


def perl_file_not_found(m):
    return MissingPerlFile(m.group(1))


class MissingMavenArtifacts(Problem):

    kind = "missing-maven-artifacts"

    def __init__(self, artifacts):
        self.artifacts = artifacts

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.artifacts == other.artifacts

    def __str__(self):
        return "Missing maven artifacts: %r" % self.artifacts

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.artifacts)


class DhUntilUnsupported(Problem):

    kind = "dh-until-unsupported"

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __str__(self):
        return "dh --until is no longer supported"

    def __repr__(self):
        return "%s()" % (type(self).__name__,)


def dh_until_unsupported(m):
    return DhUntilUnsupported()


class DhAddonLoadFailure(Problem):

    kind = "dh-addon-load-failure"

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.name == other.name
            and self.path == other.path
        )

    def __str__(self):
        return "dh addon loading failed: %s" % self.name

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.name, self.path)


def dh_addon_load_failure(m):
    return DhAddonLoadFailure(m.group(1), m.group(2))


class DhMissingUninstalled(Problem):

    kind = "dh-missing-uninstalled"

    def __init__(self, missing_file):
        self.missing_file = missing_file

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.missing_file == other.missing_file

    def __str__(self):
        return "File built by Debian not installed: %r" % self.missing_file

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.missing_file)


def dh_missing_uninstalled(m):
    return DhMissingUninstalled(m.group(2))


class DhLinkDestinationIsDirectory(Problem):

    kind = "dh-link-destination-is-directory"

    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.path == other.path

    def __str__(self):
        return "Link destination %s is directory" % self.path

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.path)


def dh_link_destination_is_dir(m):
    return DhLinkDestinationIsDirectory(m.group(1))


def maven_missing_artifact(m):
    artifacts = m.group(1).split(",")
    return MissingMavenArtifacts([a.strip() for a in artifacts])


def maven_missing_plugin(m):
    return MissingMavenArtifacts([m.group(1)])


class MissingXmlEntity(Problem):

    kind = "missing-xml-entity"

    def __init__(self, url):
        self.url = url

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.url == other.url

    def __str__(self):
        return "Missing XML entity: %s" % self.url

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.url)


def xsltproc_network_entity(m):
    return MissingXmlEntity(m.group(1))


class CcacheError(Problem):

    kind = "ccache-error"

    def __init__(self, error):
        self.error = error

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.error == other.error

    def __str__(self):
        return "ccache error: %s" % self.error

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.error)


def ccache_error(m):
    return CcacheError(m.group(1))


class MissingLibrary(Problem):

    kind = "missing-library"

    def __init__(self, library):
        self.library = library

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.library == other.library

    def __str__(self):
        return "missing library: %s" % self.library

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.library)


def ld_missing_lib(m):
    return MissingLibrary(m.group(1))


class MissingRubyGem(Problem):

    kind = "missing-ruby-gem"

    def __init__(self, gem: str, version: Optional[str] = None):
        self.gem = gem
        self.version = version

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.gem == other.gem
            and self.version == other.version
        )

    def __str__(self):
        if self.version:
            return "missing ruby gem: %s (>= %s)" % (self.gem, self.version)
        else:
            return "missing ruby gem: %s" % self.gem

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.gem, self.version)


def ruby_missing_gem(m):
    minimum_version = None
    for grp in m.group(2).split(","):
        (cond, val) = grp.strip().split(" ", 1)
        if cond == ">=":
            minimum_version = val
            break
        if cond == "~>":
            minimum_version = val
    return MissingRubyGem(m.group(1), minimum_version)


class MissingRubyFile(Problem):

    kind = "missing-ruby-file"

    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.filename)

    def __str__(self):
        return "Missing ruby file: %s" % (self.filename,)

    def __eq__(self, other):
        return isinstance(self, type(other)) and self.filename == other.filename


def ruby_missing_name(m):
    return MissingRubyFile(m.group(1))


class MissingPhpClass(Problem):

    kind = "missing-php-class"

    def __init__(self, php_class):
        self.php_class = php_class

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.php_class == other.php_class

    def __str__(self):
        return "missing PHP class: %s" % self.php_class

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.php_class)


def php_missing_class(m):
    return MissingPhpClass(m.group(1))


@problem("missing-java-class")
class MissingJavaClass:

    classname: str

    def __str__(self):
        return "missing java class: %s" % self.classname


def java_missing_class(m):
    return MissingJavaClass(m.group(1))


class MissingRPackage(Problem):

    kind = "missing-r-package"

    def __init__(self, package, minimum_version=None):
        self.package = package
        self.minimum_version = minimum_version

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.package == other.package
            and self.minimum_version == other.minimum_version
        )

    def __str__(self):
        if self.minimum_version:
            return "missing R package: %s (>= %s)" % (
                self.package,
                self.minimum_version,
            )
        else:
            return "missing R package: %s" % self.package

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.package, self.minimum_version)


def r_missing_package(m):
    fragment = m.group(1)
    deps = [dep.strip("‘’ ") for dep in fragment.split(",")]
    return MissingRPackage(deps[0])


def r_too_old(m):
    package = m.group(1)
    new_version = m.group(3)
    return MissingRPackage(package, new_version)


class FailedGoTest(Problem):

    kind = "failed-go-test"

    def __init__(self, test):
        self.test = test

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.test == other.test

    def __str__(self):
        return "failed go test: %s" % self.test

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.test)


def go_test_failed(m):
    return FailedGoTest(m.group(1))


class DebhelperPatternNotFound(Problem):

    kind = "debhelper-pattern-not-found"

    def __init__(self, pattern, tool, directories):
        self.pattern = pattern
        self.tool = tool
        self.directories = directories

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.pattern == other.pattern
            and self.tool == other.tool
            and self.directories == other.directories
        )

    def __str__(self):
        return "debhelper (%s) expansion failed for %r (directories: %r)" % (
            self.tool,
            self.pattern,
            self.directories,
        )

    def __repr__(self):
        return "%s(%r, %r, %r)" % (
            type(self).__name__,
            self.pattern,
            self.tool,
            self.directories,
        )


def dh_pattern_no_matches(m):
    return DebhelperPatternNotFound(
        m.group(2), m.group(1), [d.strip() for d in m.group(3).split(",")]
    )


class GnomeCommonMissing(Problem):

    kind = "gnome-common-missing"

    def __init__(self) -> None:
        pass

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __str__(self):
        return "gnome-common is not installed"

    def __repr__(self):
        return "%s()" % (type(self).__name__,)


def gnome_common_missing(m):
    return GnomeCommonMissing()


class MissingXfceDependency(Problem):

    kind = "missing-xfce-dependency"

    def __init__(self, package):
        self.package = package

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.package == other.package

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.package)

    def __str__(self):
        return "Missing XFCE build dependency: %s" % (self.package)


def xfce_dependency_missing(m):
    return MissingXfceDependency(m.group(1))


class MissingAutomakeInput(Problem):

    kind = "missing-automake-input"

    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.path == other.path

    def __str__(self):
        return "automake input file %s missing" % self.path

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.path)


def automake_input_missing(m):
    return MissingAutomakeInput(m.group(1))


@problem("missing-autoconf-macro")
class MissingAutoconfMacro:

    macro: str
    need_rebuild: bool = False

    def __str__(self):
        return "autoconf macro %s missing" % self.macro


def autoconf_undefined_macro(m):
    return MissingAutoconfMacro(m.group(2))


def configure_undefined_macro(m):
    return MissingAutoconfMacro(m.group(2))


class MissingGnomeCommonDependency(Problem):

    kind = "missing-gnome-common-dependency"

    def __init__(self, package, minimum_version=None):
        self.package = package
        self.minimum_version = minimum_version

    def __eq__(self, other):
        return (
            isinstance(other, type(self))
            and self.package == other.package
            and self.minimum_version == other.minimum_version
        )

    def __repr__(self):
        return "%s(%r, %r)" % (type(self).__name__, self.package, self.minimum_version)

    def __str__(self):
        return "Missing gnome-common dependency: %s: (>= %s)" % (
            self.package,
            self.minimum_version,
        )


def missing_glib_gettext(m):
    return MissingGnomeCommonDependency("glib-gettext", m.group(1))


class MissingConfigStatusInput(Problem):

    kind = "missing-config.status-input"

    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.path == other.path

    def __str__(self):
        return "missing config.status input %s" % self.path

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.path)


def config_status_input_missing(m):
    return MissingConfigStatusInput(m.group(1))


class MissingJVM(Problem):

    kind = "missing-jvm"

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(self, type(other))

    def __str__(self):
        return "Missing JVM"

    def __repr__(self):
        return "%s()" % (type(self).__name__)


def jvm_missing(m):
    return MissingJVM()


@problem("upstart-file-present")
class UpstartFilePresent:

    filename: str

    def __str__(self):
        return "Upstart file present: %s" % self.filename


def dh_installinit_upstart_file(m):
    return UpstartFilePresent(m.group(1))


@problem("need-pg-buildext-updatecontrol")
class NeedPgBuildExtUpdateControl:

    generated_path: str
    template_path: str

    def __str__(self):
        return "Need to run 'pg_buildext updatecontrol' to update %s" % (
            self.generated_path
        )


def need_pg_buildext_updatecontrol(m):
    return NeedPgBuildExtUpdateControl(m.group(1), m.group(2))


@problem("missing-vala-package")
class MissingValaPackage:

    package: str

    def __str__(self):
        return "Missing Vala package: %s" % self.package


def vala_package_missing(m):
    return MissingValaPackage(m.group(1))


MAVEN_ERROR_PREFIX = "(?:\\[ERROR\\]|\\[\x1b\\[1;31mERROR\x1b\\[m\\]) "


@problem("local-directory-not-existing")
class DirectoryNonExistant:

    path: str

    def __str__(self):
        return "Directory does not exist: %s" % self.path


def directory_not_found(m):
    return DirectoryNonExistant(m.group(1))


@problem("imagemagick-delegate-missing")
class ImageMagickDelegateMissing:

    delegate: str

    def __str__(self):
        return "Imagemagick missing delegate: %s" % self.delegate


def imagemagick_delegate_missing(m):
    return ImageMagickDelegateMissing(m.group(1))


class DebianVersionRejected(Problem):

    kind = "debian-version-rejected"

    def __init__(self, version):
        self.version = version

    def __eq__(self, other):
        return isinstance(other, type(self)) and other.version == self.version

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.version)

    def __str__(self):
        return "Debian Version Rejected; %s" % self.version


def debian_version_rejected(m):
    return DebianVersionRejected(m.group(1))


def dh_missing_addon(m):
    return DhAddonLoadFailure("pybuild", "Debian/Debhelper/Buildsystem/pybuild.pm")


class MissingHaskellDependencies(Problem):

    kind = "missing-haskell-dependencies"

    def __init__(self, deps):
        self.deps = deps

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.deps == other.deps

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.deps)

    def __str__(self):
        return "Missing Haskell dependencies: %r" % self.deps


class Matcher(object):
    def match(self, line: List[str], i: int) -> Tuple[List[int], Optional[Problem]]:
        raise NotImplementedError(self.match)


class SingleLineMatcher(Matcher):
    def __init__(self, regexp, cb=None):
        self.regexp = re.compile(regexp)
        self.cb = cb

    def match(self, lines, i):
        m = self.regexp.match(lines[i].rstrip("\n"))
        if not m:
            return [], None
        if self.cb:
            err = self.cb(m)
        else:
            err = None
        return [i], err


@problem("missing-setup.py-command")
class MissingSetupPyCommand:

    command: str

    def __str__(self):
        return "missing setup.py subcommand: %s" % self.command


class SetupPyCommandMissingMatcher(Matcher):

    final_line_re = re.compile(
        r'error: invalid command \'(.*)\'')
    warning_match = re.compile(
        r'usage: setup.py \[global_opts\] cmd1 '
        r'\[cmd1_opts\] \[cmd2 \[cmd2_opts\] \.\.\.\]')

    def match(self, lines, i):
        m = self.final_line_re.fullmatch(lines[i].rstrip('\n'))
        if not m:
            return [], None
        for j in range(i, max(0, i - 20), -1):
            if self.warning_match.fullmatch(lines[j].rstrip('\n')):
                return [i], MissingSetupPyCommand(m.group(1))
        return []


class AutoconfUnexpectedMacroMatcher(Matcher):

    regexp1 = re.compile(
        r'\.\/configure: line [0-9]+: syntax error near unexpected token `.+\'')
    regexp2 = re.compile(
        r'\.\/configure: line [0-9]+: `\s*([A-Z0-9_]+)\(.*')

    def match(self, lines, i):
        m = self.regexp1.fullmatch(lines[i].rstrip('\n'))
        if not m:
            return [], None
        try:
            m = self.regexp2.fullmatch(lines[i+1].rstrip('\n'))
        except IndexError:
            return [], None
        if m:
            return [i, i+1], MissingAutoconfMacro(m.group(1), need_rebuild=True)
        return [], None


class PythonFileNotFoundErrorMatcher(Matcher):

    final_line_re = re.compile(
        r"^(?:E  +)?FileNotFoundError: \[Errno 2\] "
        r"No such file or directory: \'(.*)\'")

    def match(self, lines, i):
        m = self.final_line_re.fullmatch(lines[i].rstrip('\n'))
        if not m:
            return [], None
        if i-2 >= 0 and 'subprocess' in lines[i-2]:
            return [i], MissingCommand(m.group(1))
        return [i], file_not_found(m)


class HaskellMissingDependencyMatcher(Matcher):

    regexp = re.compile(
        r"(.*): Encountered missing or private dependencies:"
    )

    def match(self, lines, i):
        m = self.regexp.fullmatch(lines[i].rstrip('\n'))
        if not m:
            return [], None
        deps = []
        linenos = [i]
        for line in lines[i + 1 :]:
            if not line.strip("\n"):
                break
            deps.extend([x.strip() for x in line.split(",", 1)])
            linenos.append(linenos[-1] + 1)
        return linenos, MissingHaskellDependencies(deps)


def cmake_command_missing(m):
    return MissingCommand(m.group(1).lower())


def cmake_file_missing(m):
    return MissingFile(m.group(2))


def cmake_package_config_file_missing(m):
    return CMakeFilesMissing([e.strip() for e in m.group(2).splitlines()])


def cmake_compiler_failure(m):
    compiler_output = textwrap.dedent(m.group(3))
    match, error = find_build_failure_description(
        compiler_output.splitlines(True)
    )
    return error


def cmake_compiler_missing(m):
    if m.group(1) == "Fortran":
        return MissingFortranCompiler()
    return None


class CMakeNeedExactVersion(Problem):

    kind = 'cmake-exact-version-missing'

    def __init__(self, package, version_found, exact_version_needed, path):
        self.package = package
        self.version_found = version_found
        self.exact_version_needed = exact_version_needed
        self.path = path

    def __eq__(self, other):
        return isinstance(other, type(self)) and (
            self.package == other.package and
            self.version_found == other.version_found and
            self.exact_version_needed == other.exact_version_needed and
            self.path == other.path)

    def __repr__(self):
        return "%s(%r, %r, %r, %r)" % (
            type(self).__name__,
            self.package, self.version_found,
            self.exact_version_needed,
            self.path)

    def __str__(self):
        return "CMake needs exact package %s, version %s" % (
            self.package, self.exact_version_needed)


class CMakeErrorMatcher(Matcher):

    regexp = re.compile(r"CMake Error at (.*):([0-9]+) \((.*)\):")

    cmake_errors = [
        (
            r"--  Package \'(.*)\', required by \'(.*)\', not found",
            cmake_pkg_config_missing,
        ),
        (r"Could NOT find (.*) \(missing: .*\)",
         lambda m: MissingVagueDependency(m.group(1))),
        (
            r'The (.+) compiler\n\n  "(.*)"\n\nis not able to compile a '
            r"simple test program\.\n\nIt fails with the following output:\n\n"
            r"(.*)\n\n"
            r"CMake will not be able to correctly generate this project.\n$",
            cmake_compiler_failure,
        ),
        (r"Could NOT find (.*): Found unsuitable version \"(.*)\",\sbut\s"
         r"required\sis\sexact version \"(.*)\" \(found\s(.*)\)",
         lambda m: CMakeNeedExactVersion(m.group(1), m.group(2), m.group(3), m.group(4)),
         ),
        (r"Could NOT find (.*): Found unsuitable version \"(.*)\",\sbut\s"
         r"required\sis\sat\sleast\s\"(.*)\" \(found\s(.*)\)",
         lambda m: MissingPkgConfig(m.group(1), m.group(3))
         ),
        (
            r'The imported target \"(.*)\" references the file\n\n\s*"(.*)"\n\n'
            r"but this file does not exist\.(.*)",
            cmake_file_missing,
        ),
        (
            r'Could not find a configuration file for package "(.*)".*'
            r'.*requested version "(.*)"\.',
            lambda m: MissingPkgConfig(m.group(1), m.group(2))
        ),
        (
            r'.*Could not find a package configuration file provided by "(.*)"\s'
            r"with\sany\sof\sthe\sfollowing\snames:\n\n(  .*\n)+\n.*$",
            cmake_package_config_file_missing,
        ),
        (
            r'.*Could not find a package configuration file provided by "(.*)"\s'
            r"\(requested\sversion\s.+\)\swith\sany\sof\sthe\sfollowing\snames:\n"
            r"\n(  .*\n)+\n.*$",
            cmake_package_config_file_missing,
        ),
        (
            r"No CMAKE_(.*)_COMPILER could be found.\n"
            r"\n"
            r"Tell CMake where to find the compiler by setting either"
            r'\sthe\senvironment\svariable\s"(.*)"\sor\sthe\sCMake\scache'
            r"\sentry\sCMAKE_(.*)_COMPILER\sto\sthe\sfull\spath\sto"
            r"\sthe\scompiler,\sor\sto\sthe\scompiler\sname\sif\sit\sis\sin\s"
            r"the\sPATH.\n",
            cmake_command_missing,
        ),
        (r'file INSTALL cannot find\s"(.*)".\n', lambda m: MissingFile(m.group(1))),
        (
            r'file INSTALL cannot copy file\n"(.*)"\sto\s"(.*)":\s'
            r"No space left on device.\n",
            lambda m: NoSpaceOnDevice(),
        ),
        (r'patch: \*\*\*\* write error : No space left on device',
         lambda m: NoSpaceOnDevice()),
        (r'file INSTALL cannot copy file\n"(.*)"\nto\n"(.*)"\.\n', None),
        (r'Could NOT find (.*) \(missing: (.*)\)', None),
        (r'Missing (.*)\.  Either your\n'
         r'lib(.*) version is too old, or lib(.*) wasn\'t found in the place you\n'
         r'said.', lambda m: MissingLibrary(m.group(1))),
        (r'need (.*) of version (.*)',
         lambda m: MissingVagueDependency(m.group(1), minimum_version=m.group(2).strip())),
    ]

    @classmethod
    def _extract_error_lines(cls, lines, i):
        linenos = [i]
        error_lines = []
        for j, line in enumerate(lines[i + 1 :]):
            if line != "\n" and not line.startswith(" "):
                break
            error_lines.append(line)
            linenos.append(i + 1 + j)
        while error_lines and error_lines[-1] == "\n":
            error_lines.pop(-1)
            linenos.pop(-1)
        return linenos, textwrap.dedent("".join(error_lines)).splitlines(True)

    def match(self, lines, i):
        m = self.regexp.fullmatch(lines[i].rstrip('\n'))
        if not m:
            return [], None

        path = m.group(1)  # noqa: F841
        start_lineno = int(m.group(2))  # noqa: F841
        linenos, error_lines = self._extract_error_lines(lines, i)

        error = None
        for r, fn in self.cmake_errors:
            m = re.match(r, "".join(error_lines), flags=re.DOTALL)
            if m:
                if fn is None:
                    error = None
                else:
                    error = fn(m)
                break

        return linenos, error


class MissingFortranCompiler(Problem):

    kind = "missing-fortran-compiler"

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __str__(self):
        return "No Fortran compiler found"

    def __repr__(self):
        return "%s()" % type(self).__name__


class MissingCSharpCompiler(Problem):

    kind = "missing-c#-compiler"

    def __init__(self):
        pass

    def __eq__(self, other):
        return isinstance(other, type(self))

    def __str__(self):
        return "No C# compiler found"

    def __repr__(self):
        return "%s()" % type(self).__name__


def c_sharp_compiler_missing(m):
    return MissingCSharpCompiler()


@problem("missing-libtool")
class MissingLibtool:

    def __str__(self):
        return "Libtool is missing"


@problem("missing-pytest-fixture")
class MissingPytestFixture:

    fixture: str

    def __str__(self):
        return "Missing pytest fixture: %s" % self.fixture


@problem("missing-cargo-crate")
class MissingCargoCrate:

    crate: str
    requirement: Optional[str]

    def __str__(self):
        if self.requirement:
            return "Missing crate: %s (%s)" % (self.crate, self.requirement)
        else:
            return "Missing crate: %s" % self.crate


def cargo_missing_requirement(m):
    try:
        crate, requirement = m.group(1).split(" ", 1)
    except ValueError:
        crate = m.group(1)
        requirement = None
    return MissingCargoCrate(crate, requirement)


def missing_lazyfont_file(m):
    return MissingFile(m.group(1))


@problem("missing-dh-compat-level")
class MissingDHCompatLevel:

    command: str

    def __str__(self):
        return "Missing DH Compat Level (command: %s)" % self.command


@problem("duplicate-dh-compat-level")
class DuplicateDHCompatLevel:

    command: str

    def __str__(self):
        return "DH Compat Level specified twice (command: %s)" % self.command


class UnknownCertificateAuthority(Problem):

    kind = "unknown-certificate-authority"

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.url)

    def __str__(self):
        return "Unknown Certificate Authority for %s" % self.url

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.url == other.url


build_failure_regexps = [
    (
        r"make\[[0-9]+\]: \*\*\* No rule to make target "
        r"\'(.*)\', needed by \'.*\'\.  Stop\.",
        file_not_found,
    ),
    (
        r"make: \*\*\* No rule to make target "
        r"\'(\/.*)\'\.  Stop\.",
        file_not_found,
    ),
    (r"[^:]+:\d+: (.*): No such file or directory", file_not_found),
    (
        r"(distutils.errors.DistutilsError|error): "
        r"Could not find suitable distribution "
        r"for Requirement.parse\(\'([^\']+)\'\)",
        python_reqs_not_found,
    ),
    (
        r'We need the Python library (.*) to be installed. '
        r'Try runnning: python -m ensurepip',
        lambda m: MissingPythonDistribution(m.group(1)),
    ),
    (
        r'pkg_resources.DistributionNotFound: The \'([^\']+)\' '
        r'distribution was not found and is required by the application',
        pkg_resources_distribution_not_found,
    ),
    (
        r"pkg_resources.DistributionNotFound: The \'([^\']+)\' "
        r"distribution was not found and is required by (.*)",
        pkg_resources_distribution_not_found,
    ),
    (
        r"Please install cmake version \>= (.*) and re-run setup",
        lambda m: MissingCommand('cmake'),
    ),
    (
        r"pluggy.manager.PluginValidationError: "
        r"Plugin \'.*\' could not be loaded: "
        r"\(.* \(/usr/lib/python2.[0-9]/dist-packages\), "
        r"Requirement.parse\(\'(.*)\'\)\)\!",
        python2_reqs_not_found,
    ),
    ("ImportError: cannot import name '(.*)' from '(.*)'", python_submodule_not_found),
    ("E       fixture '(.*)' not found",
        lambda m: MissingPytestFixture(m.group(1))),
    ("E   ImportError: cannot import name '(.*)' from '(.*)'", python_submodule_not_found),
    ("E   ImportError: cannot import name ([^']+)", python_module_not_found),
    (
        r"django.core.exceptions.ImproperlyConfigured: Error loading .* module: "
        r"No module named \'(.*)\'",
        python_module_not_found,
    ),
    ("E   ImportError: No module named (.*)", python_module_not_found),
    (r"\s*ModuleNotFoundError: No module named '(.*)'", python3_module_not_found),
    (
        r"Could not import extension .* \(exception: No module named (.*)\)",
        sphinx_module_not_found,
    ),
    (r"^(.*): Error while finding module specification for "
     r"'(.*)' \(ModuleNotFoundError: No module named '(.*)'\)",
     python_cmd_module_not_found
     ),
    ("E   ModuleNotFoundError: No module named '(.*)'", python3_module_not_found),
    (r"/usr/bin/python3: No module named (.*)", python3_module_not_found),
    ('.*:[0-9]+: cannot find package "(.*)" in any of:', missing_go_package),
    (
        r'ImportError: Error importing plugin ".*": No module named (.*)',
        python_module_not_found,
    ),
    ("ImportError: No module named (.*)", python_module_not_found),
    (
        r"[^:]+:\d+:\d+: fatal error: (.+\.h|.+\.hpp): No such file or directory",
        c_header_missing,
    ),
    (
        r"[^:]+\.[ch]:\d+:\d+: fatal error: (.+): No such file or directory",
        c_header_missing,
    ),
    ("✖ \x1b\\[31mERROR:\x1b\\[39m Cannot find module '(.*)'", node_module_missing),
    ('\\[31mError: No test files found: "(.*)"\\[39m', None),
    (r'\x1b\[31mError: No test files found: "(.*)"\x1b\[39m', None),
    (r"\s*Error: Cannot find module \'(.*)\'", node_module_missing),
    (r">> Error: Cannot find module \'(.*)\'", node_module_missing),
    (
        r">> Got an unexpected exception from the coffee-script compiler. "
        r"The original exception was: Error: Cannot find module \'(.*)\'",
        node_module_missing,
    ),
    (
        r"\s*Module not found: Error: Can\'t resolve \'(.*)\' in \'(.*)\'",
        node_module_missing,
    ),
    (r'qmake: could not find a Qt installation of \'\'',
     lambda m: MissingQt()),
    (r'Cannot find X include files via .*', lambda m: MissingX11()),
    (r'\*\*\* No X11\! Install X-Windows development headers/libraries\! \*\*\*',
     lambda m: MissingX11()),
    (r'  \*\*\* The (.*) script could not be found\. .*',
     lambda m: MissingCommand(m.group(1))),
    (r'>> Local Npm module \"(.*)" not found. Is it installed?', node_module_missing),
    (r"npm ERR\! \[\!\] Error: Cannot find module '(.*)'",
     node_module_missing),
    (r'npm ERR\! \>\> Local Npm module "(.*)" not found. Is it installed\?',
     node_module_missing),
    (r"npm ERR\! Error: Cannot find module '(.*)'",
     node_module_missing),
    (r"npm ERR\! ERROR in Entry module not found: "
     r"Error: Can't resolve '(.*)' in '.*'", node_module_missing),
    (r"(\.\/configure): line \d+: ([A-Z0-9_]+): command not found", configure_undefined_macro),
    (r".*: line \d+: ([^ ]+): command not found", command_missing),
    (r".*: line \d+: ([^ ]+): Permission denied", None),
    (r"\/bin\/sh: \d+: ([^ ]+): not found", command_missing),
    (r"sh: \d+: ([^ ]+): not found", command_missing),
    (r".*\.sh: \d+: ([^ ]+): not found", command_missing),
    (r".*: 1: cd: can\'t cd to (.*)", directory_not_found),
    (r"\/bin\/bash: (.*): command not found", command_missing),
    (r"bash: (.*): command not found", command_missing),
    (r"env: ‘(.*)’: No such file or directory", interpreter_missing),
    (
        r"\/bin\/bash: .*: (.*): bad interpreter: No such file or directory",
        interpreter_missing,
    ),
    # SH error
    (r".*: [0-9]+: exec: (.*): not found", command_missing),
    (r".*: [0-9]+: (.*): not found", command_missing),
    (r"/usr/bin/env: ‘(.*)’: No such file or directory", command_missing),
    (r"/usr/bin/env: \'(.*)\': No such file or directory", command_missing),
    (r"make\[[0-9]+\]: (.*): Command not found", command_missing),
    (r"make: (.*): Command not found", command_missing),
    (r"make: (.*): No such file or directory", command_missing),
    (r"xargs: (.*): No such file or directory", command_missing),
    (r"make\[[0-9]+\]: ([^/ :]+): No such file or directory", command_missing),
    (r".*: failed to exec \'(.*)\': No such file or directory", command_missing),
    (r"No package \'([^\']+)\' found", pkg_config_missing),
    (r"\-\- Please install Git, make sure it is in your path, and then try again.",
     lambda m: MissingCommand('git')),
    (r'\> Cannot run program "(.*)": error=2, No such file or directory',
     lambda m: MissingCommand(m.group(1))),
    ("Please install 'git' seperately and try again.",
     lambda m: MissingCommand('git')),
    (r'\> A problem occurred starting process \'command \'(.*)\'\'',
     lambda m: MissingCommand(m.group(1))),
    (r'vcver.scm.git.GitCommandError: \'git .*\' returned an error code 127',
     lambda m: MissingCommand('git')),
    (r"configure: error: No package \'([^\']+)\' found", pkg_config_missing),
    (
        r"configure: error: (doxygen|asciidoc) is not available "
        r"and maintainer mode is enabled",
        lambda m: MissingCommand(m.group(1)),
    ),
    (
        r"configure: error: Documentation enabled but rst2html not found.",
        lambda m: MissingCommand("rst2html"),
    ),
    (r'cannot run pkg-config to check .* version at (.*) line [0-9]+\.',
     lambda m: MissingCommand('pkg-config')),
    (r"Error: pkg-config not found\!", lambda m: MissingCommand("pkg-config")),
    (r"ERROR: unable to find python", lambda m: MissingCommand("python")),
    (r" ERROR: BLAS not found\!", lambda m: MissingLibrary("blas")),
    AutoconfUnexpectedMacroMatcher(),
    (r"\./configure: [0-9]+: \.: Illegal option .*", None),
    (r"Requested \'(.*)\' but version of ([^ ]+) is ([^ ]+)", pkg_config_missing),
    (
        r"configure: error: Package requirements \((.*)\) were not met:",
        pkg_config_missing,
    ),
    (
        r"configure: error: [a-z0-9_-]+-pkg-config (.*) couldn\'t be found",
        pkg_config_missing,
    ),
    (r'configure: error: C preprocessor "/lib/cpp" fails sanity check', None),
    (
        r"configure: error: .*\. Please install (bison|flex)",
        lambda m: MissingCommand(m.group(1)),
    ),
    (
        r"configure: error: No C\# compiler found. You need to install either "
        r"mono \(>=(.*)\) or \.Net",
        c_sharp_compiler_missing,
    ),
    (r"configure: error: gmcs Not found", c_sharp_compiler_missing),
    (r"configure: error: You need to install gmcs", c_sharp_compiler_missing),
    (
        r"configure: error: (.*) requires libkqueue \(or system kqueue\). .*",
        lambda m: MissingPkgConfig("libkqueue"),
    ),
    (
        r'Did not find pkg-config by name \'pkg-config\'',
        lambda m: MissingCommand('pkg-config'),
    ),
    (
        '.*meson.build:([0-9]+):([0-9]+): ERROR: Dependency "(.*)" not found',
        meson_pkg_config_missing,
    ),
    (
        '.*meson.build:([0-9]+):([0-9]+): ERROR: Dependency "(.*)" not found, '
        "tried pkgconfig",
        meson_pkg_config_missing,
    ),
    (
        ".*meson.build:([0-9]+):([0-9]+): ERROR: Invalid version of dependency, "
        "need '([^']+)' \\['>= ([^']+)'\\] found '([^']+)'\\.",
        meson_pkg_config_too_low,
    ),
    (
        ".*meson.build:([0-9]+):([0-9]+): ERROR: C shared or static library '(.*)' not found",
        meson_c_library_missing,
    ),
    (
        ".*meson.build:([0-9]+):([0-9]+): ERROR: Pkg-config binary for machine .* not found. Giving up.",
        lambda m: MissingCommand('pkg-config'),
    ),
    (
        r"dh: Unknown sequence --(.*) "
        r"\(options should not come before the sequence\)",
        dh_with_order,
    ),
    (
        r"dh: Compatibility levels before [0-9]+ are no longer supported "
        r"\(level [0-9]+ requested\)",
        None,
    ),
    (r"dh: Unknown sequence (.*) \(choose from: .*\)", None),
    (r".*: .*: No space left on device", install_no_space),
    (r"^No space left on device.", install_no_space),
    (
        r".*Can\'t locate (.*).pm in @INC \(you may need to install the "
        r"(.*) module\) \(@INC contains: (.*)\) at .* line .*.",
        perl_missing_module,
    ),
    (r">\(error\): Could not expand \[(.*)\'", perl_expand_failed),
    (
        r"\[DZ\] could not load class (.*) for license (.*)",
        lambda m: MissingPerlModule(None, m.group(1), None),
    ),
    (r"Required plugin bundle ([^ ]+) isn\'t installed.", perl_missing_plugin),
    (r"Required plugin ([^ ]+) isn\'t installed.", perl_missing_plugin),
    (
        r".*Can\'t locate (.*) in @INC \(@INC contains: (.*)\) at .* line .*.",
        perl_missing_file,
    ),
    (
        r"Can\'t find author dependency (.*) at (.*) line ([0-9]+).",
        perl_missing_author_dep,
    ),
    (
        r"> Could not find (.*)\. Please check that (.*) contains a valid JDK "
        r"installation.",
        jdk_file_missing,
    ),
    (
        r"> Could not find (.*)\. Please check that (.*) contains a valid "
        r"\(and compatible\) JDK installation.",
        jdk_file_missing,
    ),
    (
        r"> Kotlin could not find the required JDK tools in the Java "
        r"installation '(.*)' used by Gradle. Make sure Gradle is running "
        "on a JDK, not JRE.",
        jdk_missing,
    ),
    (
        r"ERROR: JAVA_HOME is not set and no 'java' command could be found "
        r"in your PATH.",
        jre_missing
    ),
    (
        r"(?:/usr/bin/)?install: cannot create regular file \'(.*)\': "
        r"No such file or directory",
        None,
    ),
    (
        r"python[0-9.]*: can\'t open file \'(.*)\': \[Errno 2\] "
        r"No such file or directory",
        file_not_found,
    ),
    (r'.*:[0-9]+:[0-9]+: ERROR: \<ExternalProgram \'python3\' -> '
     r'\[\'/usr/bin/python3\'\]\> is not a valid python or '
     r'it is missing setuptools',
     lambda m: MissingPythonDistribution('setuptools', python_version=3)
     ),
    (r"OSError: \[Errno 28\] No space left on device", lambda m: NoSpaceOnDevice()),
    # python:setuptools_scm
    (r"OSError: 'git' was not found", lambda m: MissingCommand('git')),
    (r"OSError: No such file (.*)", file_not_found),
    (
        r"Could not open \'(.*)\': No such file or directory at "
        r"\/usr\/share\/perl\/[0-9.]+\/ExtUtils\/MM_Unix.pm line [0-9]+.",
        perl_file_not_found,
    ),
    (r'Can\'t open perl script "(.*)": No such file or directory', perl_file_not_found),
    # Maven
    (
        MAVEN_ERROR_PREFIX + r"Failed to execute goal on project .*: "
        r"Could not resolve dependencies for project .*: "
        r"The following artifacts could not be resolved: (.*): "
        r"Cannot access central \(https://repo\.maven\.apache\.org/maven2\) "
        r"in offline mode and the artifact .* has not been downloaded from "
        r"it before..*",
        maven_missing_artifact,
    ),
    (
        MAVEN_ERROR_PREFIX + r"Unresolveable build extension: "
        r"Plugin (.*) or one of its dependencies could not be resolved: "
        r"Cannot access central \(https://repo.maven.apache.org/maven2\) "
        r"in offline mode and the artifact .* has not been downloaded "
        "from it before. @",
        maven_missing_plugin,
    ),
    (
        MAVEN_ERROR_PREFIX + r"Non-resolvable import POM: Cannot access central "
        r"\(https://repo.maven.apache.org/maven2\) in offline mode and the "
        r"artifact (.*) has not been downloaded from it before. "
        r"@ line [0-9]+, column [0-9]+",
        maven_missing_artifact,
    ),
    (
        r"\[FATAL\] Non-resolvable parent POM for .*: Cannot access central "
        r"\(https://repo.maven.apache.org/maven2\) in offline mode and the "
        "artifact (.*) has not been downloaded from it before. .*",
        maven_missing_artifact,
    ),
    (
        MAVEN_ERROR_PREFIX + r"Plugin (.*) or one of its dependencies could "
        r"not be resolved: Cannot access central "
        r"\(https://repo.maven.apache.org/maven2\) in offline mode and the "
        r"artifact .* has not been downloaded from it before. -> \[Help 1\]",
        maven_missing_plugin,
    ),
    (
        MAVEN_ERROR_PREFIX + r"Failed to execute goal on project .*: "
        r"Could not resolve dependencies for project .*: Cannot access "
        r".* \([^\)]+\) in offline mode and the artifact "
        r"(.*) has not been downloaded from it before. -> \[Help 1\]",
        maven_missing_artifact,
    ),
    (
        MAVEN_ERROR_PREFIX + r"Failed to execute goal on project .*: "
        r"Could not resolve dependencies for project .*: Cannot access central "
        r"\(https://repo.maven.apache.org/maven2\) in offline mode and the "
        r"artifact (.*) has not been downloaded from it before..*",
        maven_missing_artifact,
    ),
    (MAVEN_ERROR_PREFIX + "Failed to execute goal (.*) on project (.*): (.*)", None),
    (
        MAVEN_ERROR_PREFIX
        + r"Error resolving version for plugin \'(.*)\' from the repositories "
        r"\[.*\]: Plugin not found in any plugin repository -> \[Help 1\]",
        maven_missing_plugin,
    ),
    (
        r"(.*): exec: \"(.*)\": executable file not found in \$PATH",
        lambda m: MissingCommand(m.group(2))
    ),
    (
        r"Can't exec \"(.*)\": No such file or directory at (.*) line ([0-9]+)\.",
        command_missing,
    ),
    (
        r"dh_missing: (warning: )?(.*) exists in debian/.* but is not "
        r"installed to anywhere",
        dh_missing_uninstalled,
    ),
    (r"dh_link: link destination (.*) is a directory", dh_link_destination_is_dir),
    (r"I/O error : Attempt to load network entity (.*)", xsltproc_network_entity),
    (r"ccache: error: (.*)", ccache_error),
    (
        r"dh: The --until option is not supported any longer \(#932537\). "
        r"Use override targets instead.",
        dh_until_unsupported,
    ),
    (
        r"dh: unable to load addon (.*): (.*) did not return a true "
        r"value at \(eval 11\) line ([0-9]+).",
        dh_addon_load_failure,
    ),
    (
        "ERROR: dependencies (.*) are not available for package ‘(.*)’",
        r_missing_package,
    ),
    ("ERROR: dependency ‘(.*)’ is not available for package ‘(.*)’", r_missing_package),
    (
        r"Error in library\(.*\) : there is no package called \'(.*)\'",
        r_missing_package,
    ),
    (r"there is no package called \'(.*)\'", r_missing_package),
    (
        r"  namespace ‘(.*)’ ([^ ]+) is being loaded, but >= ([^ ]+) is required",
        r_too_old,
    ),
    (
        r"  namespace ‘(.*)’ ([^ ]+) is already loaded, but >= ([^ ]+) " r"is required",
        r_too_old,
    ),
    (r"mv: cannot stat \'(.*)\': No such file or directory", file_not_found),
    (r"mv: cannot move \'.*\' to \'(.*)\': No such file or directory", None),
    (
        r"(/usr/bin/install|mv): "
        r"will not overwrite just-created \'(.*)\' with \'(.*)\'",
        None,
    ),
    (r"IOError: \[Errno 2\] No such file or directory: \'(.*)\'", file_not_found),
    (r"error: \[Errno 2\] No such file or directory: \'(.*)\'", file_not_found),
    (r"E   IOError: \[Errno 2\] No such file or directory: \'(.*)\'", file_not_found),
    ("FAIL\t(.+\\/.+\\/.+)\t([0-9.]+)s", go_test_failed),
    (
        r'dh_(.*): Cannot find \(any matches for\) "(.*)" \(tried in (.*)\)',
        dh_pattern_no_matches,
    ),
    (
        r'Can\'t exec "(.*)": No such file or directory at '
        r"/usr/share/perl5/Debian/Debhelper/Dh_Lib.pm line [0-9]+.",
        command_missing,
    ),
    (r".*: error: (.*) command not found", command_missing),
    (
        r"dh_install: Please use dh_missing " "--list-missing/--fail-missing instead",
        None,
    ),
    (
        r'dh([^:]*): Please use the third-party "pybuild" build system '
        "instead of python-distutils",
        None,
    ),
    # A Python error, but not likely to be actionable. The previous
    # line will have the actual line that failed.
    (r"ImportError: cannot import name (.*)", None),
    (r"/usr/bin/ld: cannot find -l(.*)", ld_missing_lib),
    (
        r"Could not find gem \'([^ ]+) \(([^)]+)\)\', " r"which is required by gem.*",
        ruby_missing_gem,
    ),
    (
        r"Could not find gem \'([^ \']+)\', " r"which is required by gem.*",
        lambda m: MissingRubyGem(m.group(1)),
    ),
    (
        r"[^:]+:[0-9]+:in \`to_specs\': Could not find \'(.*)\' \(([^)]+)\) "
        r"among [0-9]+ total gem\(s\) \(Gem::MissingSpecError\)",
        ruby_missing_gem,
    ),
    (
        r"[^:]+:[0-9]+:in \`to_specs\': Could not find \'(.*)\' \(([^)]+)\) "
        r"- .* \(Gem::MissingSpecVersionError\)",
        ruby_missing_gem,
    ),
    (
        r"[^:]+:[0-9]+:in \`block in verify_gemfile_dependencies_are_found\!\': "
        r"Could not find gem \'(.*)\' in any of the gem sources listed in "
        r"your Gemfile\. \(Bundler::GemNotFound\)",
        lambda m: MissingRubyGem(m.group(1)),
    ),
    (
        r"[^:]+:[0-9]+:in \`find_spec_for_exe\': can\'t find gem "
        r"(.*) \(([^)]+)\) with executable (.*) \(Gem::GemNotFoundException\)",
        ruby_missing_gem,
    ),
    (
        r"PHP Fatal error:  Uncaught Error: Class \'(.*)\' not found in "
        r"(.*):([0-9]+)",
        php_missing_class,
    ),
    (r"Caused by: java.lang.ClassNotFoundException: (.*)", java_missing_class),
    (
        r"\[(.*)\] \t\t:: (.*)\#(.*);\$\{(.*)\}: not found",
        lambda m: MissingMavenArtifacts(
            ["%s:%s:jar:debian" % (m.group(2), m.group(3))]
        ),
    ),
    (
        r"Caused by: java.lang.IllegalArgumentException: "
        r"Cannot find JAR \'(.*)\' required by module \'(.*)\' "
        r"using classpath or distribution directory \'(.*)\'",
        None,
    ),
    (
        r".*\.xml:[0-9]+: Unable to find a javac compiler;",
        lambda m: MissingJavaClass("com.sun.tools.javac.Main"),
    ),
    (
        r'checking for (.*)\.\.\. configure: error: "Cannot check for existence of module (.*) without pkgconf"',
        lambda m: MissingCommand('pkgconf'),
    ),
    (
        r'autoreconf was not found; .*',
        lambda m: MissingCommand('autoreconf'),
    ),
    (
        r"python3.[0-9]+: can\'t open file \'(.*)\': "
        "[Errno 2] No such file or directory",
        file_not_found,
    ),
    (r"g\+\+: error: (.*): No such file or directory", file_not_found),
    (r"strip: \'(.*)\': No such file", file_not_found),
    (
        r"Sprockets::FileNotFound: couldn\'t find file \'(.*)\' " r"with type \'(.*)\'",
        sprockets_file_not_found,
    ),
    (
        r'xdt-autogen: You must have "(.*)" installed. You can get if from',
        xfce_dependency_missing,
    ),
    (
        r'autogen.sh: You must have GNU autoconf installed.',
        lambda m: MissingCommand('autoconf'),
    ),
    (
        r'\s*You must have (autoconf|automake|aclocal|libtool|libtoolize) installed to compile (.*)\.',
        lambda m: MissingCommand(m.group(1)),
    ),
    (
        r'It appears that Autotools is not correctly installed on this system.',
        lambda m: MissingCommand('autoconf'),
    ),
    (
        r'\*\*\* No autoreconf found \*\*\*',
        lambda m: MissingCommand('autoreconf'),
    ),
    (r"You need to install the gnome-common module and make.*", gnome_common_missing),
    (
        r"You need to install gnome-common from the GNOME (git|CVS|SVN)",
        gnome_common_missing,
    ),
    (
        r"automake: error: cannot open < (.*): No such file or directory",
        automake_input_missing,
    ),
    (
        r"configure.(in|ac):[0-9]+: error: possibly undefined macro: (.*)",
        autoconf_undefined_macro,
    ),
    (
        r"configure.(in|ac):[0-9]+: error: macro (.*) is not defined; "
        r"is a m4 file missing\?",
        autoconf_undefined_macro
    ),
    (
        r"config.status: error: cannot find input file: `(.*)\'",
        config_status_input_missing,
    ),
    (
        r"\*\*\*Error\*\*\*: You must have glib-gettext >= (.*) installed.*",
        missing_glib_gettext,
    ),
    (
        r"ERROR: JAVA_HOME is set to an invalid directory: "
        r"/usr/lib/jvm/default-java/",
        jvm_missing,
    ),
    (
        r"dh_installdocs: --link-doc not allowed between (.*) and (.*) "
        r"\(one is arch:all and the other not\)",
        None,
    ),
    (
        r"dh: unable to load addon systemd: dh: The systemd-sequence is "
        "no longer provided in compat >= 11, please rely on dh_installsystemd "
        "instead",
        None,
    ),
    (
        r"dh: The --before option is not supported any longer \(#932537\). "
        r"Use override targets instead.",
        None,
    ),
    ("(.*):([0-9]+): undefined reference to `(.*)'", None),
    ("(.*):([0-9]+): error: undefined reference to '(.*)'", None),
    (
        r"\/usr\/bin\/ld: (.*): multiple definition of `*.\'; "
        r"(.*): first defined here",
        None,
    ),
    (r"\/usr\/bin\/ld: (.*): undefined reference to `(.*)\'", None),
    (r"\/usr\/bin\/ld: (.*): undefined reference to symbol \'(.*)\'", None),
    (
        r"\/usr\/bin\/ld: (.*): relocation (.*) against symbol `(.*)\' "
        r"can not be used when making a shared object; recompile with -fPIC",
        None,
    ),
    (
        "(.*):([0-9]+): multiple definition of `(.*)'; (.*):([0-9]+): "
        "first defined here",
        None,
    ),
    (
        "(dh.*): debhelper compat level specified both in debian/compat "
        "and via build-dependency on debhelper-compat",
        lambda m: DuplicateDHCompatLevel(m.group(1)),
    ),
    (
        "(dh.*): (error: )?Please specify the compatibility level in " "debian/compat",
        lambda m: MissingDHCompatLevel(m.group(1)),
    ),
    (
        "dh_makeshlibs: The udeb (.*) does not contain any shared libraries "
        "but --add-udeb=(.*) was passed!?",
        None,
    ),
    (
        "dpkg-gensymbols: error: some symbols or patterns disappeared in the "
        "symbols file: see diff output below",
        None,
    ),
    (
        r"Failed to copy \'(.*)\': No such file or directory at "
        r"/usr/share/dh-exec/dh-exec-install-rename line [0-9]+.*",
        file_not_found,
    ),
    (r"Invalid gemspec in \[.*\]: No such file or directory - (.*)", command_missing),
    (
        r".*meson.build:[0-9]+:[0-9]+: ERROR: Program\(s\) \[\'(.*)\'\] not "
        r"found or not executable",
        command_missing,
    ),
    (
        r".*meson.build:[0-9]+:[0-9]: ERROR: Git program not found\.",
        lambda m: MissingCommand("git"),
    ),
    (
        r"dpkg-gensymbols: error: some symbols or patterns disappeared in "
        r"the symbols file: see diff output below",
        None,
    ),
    (
        r"Failed: [pytest] section in setup.cfg files is no longer "
        r"supported, change to [tool:pytest] instead.",
        None,
    ),
    (r"cp: cannot stat \'(.*)\': No such file or directory", None),
    (r"cp: \'(.*)\' and \'(.*)\' are the same file", None),
    (r"PHP Fatal error: (.*)", None),
    (r"sed: no input files", None),
    (r"sed: can\'t read (.*): No such file or directory", file_not_found),
    (
        r"ERROR in Entry module not found: Error: Can\'t resolve "
        r"\'(.*)\' in \'(.*)\'",
        webpack_file_missing,
    ),
    (
        r".*:([0-9]+): element include: XInclude error : "
        r"could not load (.*), and no fallback was found",
        None,
    ),
    (r'E: Failed to execute “(.*)”: No such file or directory', command_missing),
    (r"E: The Debian version .* cannot be used as an ELPA version.", None),
    # ImageMagick
    (
        r"convert convert: Image pixel limit exceeded "
        r"\(see -limit Pixels\) \(-1\).",
        None,
    ),
    (r"convert convert: Improper image header \(.*\).", None),
    (r"convert convert: invalid primitive argument \([0-9]+\).", None),
    (r"convert convert: Unexpected end-of-file \(\)\.", None),
    (r"ERROR: Sphinx requires at least Python (.*) to run.", None),
    (
        r"convert convert: No encode delegate for this image format \((.*)\) "
        r"\[No such file or directory\].",
        imagemagick_delegate_missing,
    ),
    (r"Can\'t find (.*) directory in (.*)", None),
    (
        r"/bin/sh: [0-9]: cannot create (.*): Directory nonexistent",
        lambda m: DirectoryNonExistant(os.path.dirname(m.group(1))),
    ),
    (r"dh: Unknown sequence (.*) \(choose from: .*\)", None),
    (r".*\.vala:[0-9]+\.[0-9]+-[0-9]+.[0-9]+: error: (.*)", None),
    (
        r"error: Package `(.*)\' not found in specified Vala API directories "
        r"or GObject-Introspection GIR directories",
        vala_package_missing,
    ),
    (r".*.scala:[0-9]+: error: (.*)", None),
    # JavaScript
    (r"error TS6053: File \'(.*)\' not found.", file_not_found),
    (r"(.*\.ts)\([0-9]+,[0-9]+\): error TS[0-9]+: (.*)", None),
    (r"(.*.nim)\([0-9]+, [0-9]+\) Error: .*", None),
    (
        r"dh_installinit: upstart jobs are no longer supported\!  "
        r"Please remove (.*) and check if you need to add a conffile removal",
        dh_installinit_upstart_file,
    ),
    (
        r"dh_installinit: --no-restart-on-upgrade has been renamed to "
        "--no-stop-on-upgrade",
        None,
    ),
    (r"find: paths must precede expression: .*", None),
    (r"find: ‘(.*)’: No such file or directory", file_not_found),
    (r"ninja: fatal: posix_spawn: Argument list too long", None),
    ("ninja: fatal: chdir to '(.*)' - No such file or directory", directory_not_found),
    # Java
    (r"error: Source option [0-9] is no longer supported. Use [0-9] or later.", None),
    (
        r"(dh.*|jh_build): -s/--same-arch has been removed; "
        r"please use -a/--arch instead",
        None,
    ),
    (
        r"dh_systemd_start: dh_systemd_start is no longer used in "
        r"compat >= 11, please use dh_installsystemd instead",
        None,
    ),
    (r"Trying patch (.*) at level 1 \.\.\. 0 \.\.\. 2 \.\.\. failure.", None),
    # QMake
    (r"Project ERROR: Unknown module\(s\) in QT: (.*)", None),
    (r"Project ERROR: (.*) development package not found", pkg_config_missing),
    (r"Package \'(.*)\', required by \'(.*)\', not found\n", pkg_config_missing),
    (r"pkg-config cannot find (.*)", pkg_config_missing),
    (
        r"configure: error: .* not found: Package dependency requirement "
        r"\'([^\']+)\' could not be satisfied.",
        pkg_config_missing,
    ),
    (
        r"configure: error: (.*) is required to build documentation",
        lambda m: MissingVagueDependency(m.group(1)),
    ),
    (r".*:[0-9]+: (.*) does not exist.", file_not_found),
    # uglifyjs
    (r"ERROR: can\'t read file: (.*)", file_not_found),
    (r'jh_build: Cannot find \(any matches for\) "(.*)" \(tried in .*\)', None),
    (
        r"--   Package \'(.*)\', required by \'(.*)\', not found",
        lambda m: MissingPkgConfig(m.group(1)),
    ),
    (
        r".*.rb:[0-9]+:in `require_relative\': cannot load such file "
        r"-- (.*) \(LoadError\)",
        None,
    ),
    (
        r".*.rb:[0-9]+:in `require\': cannot load such file " r"-- (.*) \(LoadError\)",
        ruby_missing_name,
    ),
    (r"LoadError: cannot load such file -- (.*)", ruby_missing_name),
    (r"  cannot load such file -- (.*)", ruby_missing_name),
    # TODO(jelmer): This is a fairly generic string; perhaps combine with other
    # checks for ruby?
    (r"File does not exist: ([a-z/]+)$", ruby_missing_name),
    (
        r".*:[0-9]+:in `do_check_dependencies\': E: "
        r"dependency resolution check requested but no working "
        r"gemspec available \(RuntimeError\)",
        None,
    ),
    (r"rm: cannot remove \'(.*)\': Is a directory", None),
    (r"rm: cannot remove \'(.*)\': No such file or directory", None),
    # Invalid option from Python
    (r"error: option .* not recognized", None),
    # Invalid option from go
    (r"flag provided but not defined: .*", None),
    (r'CMake Error: The source directory "(.*)" does not exist.', directory_not_found),
    (r".*: [0-9]+: cd: can\'t cd to (.*)", directory_not_found),
    (r"/bin/sh: 0: Can\'t open (.*)", file_not_found),
    (r"/bin/sh: [0-9]+: cannot open (.*): No such file", file_not_found),
    (r".*: line [0-9]+: (.*): No such file or directory", file_not_found),
    (r"error: No member named \$memberName", None),
    (
        r"(?:/usr/bin/)?install: cannot create regular file \'(.*)\': "
        r"Permission denied",
        None,
    ),
    (r"(?:/usr/bin/)?install: cannot create directory .(.*).: File exists", None),
    (r"/usr/bin/install: missing destination file operand after .*", None),
    # Ruby
    (r"rspec .*\.rb:[0-9]+ # (.*)", None),
    # help2man
    (r"Addendum (.*) does NOT apply to (.*) \(translation discarded\).", None),
    (
        r"dh_installchangelogs: copy\((.*), (.*)\): No such file or directory",
        file_not_found,
    ),
    (r"dh_installman: mv (.*) (.*): No such file or directory", file_not_found),
    (r"dh_installman: Could not determine section for (.*)", None),
    (
        r"failed to initialize build cache at (.*): mkdir (.*): " r"permission denied",
        None,
    ),
    (
        r'Can\'t exec "(.*)": No such file or directory at (.*) line ([0-9]+).',
        command_missing,
    ),
    # PHPUnit
    (r'Cannot open file "(.*)".', file_not_found),
    (
        r".*Could not find a JavaScript runtime\. See "
        r"https://github.com/rails/execjs for a list of available runtimes\..*",
        javascript_runtime_missing,
    ),
    PythonFileNotFoundErrorMatcher(),
    # ruby
    (r"Errno::ENOENT: No such file or directory - (.*)", file_not_found),
    (r"(.*.rb):[0-9]+:in `.*\': .* \(.*\) ", None),
    # JavaScript
    (r".*: ENOENT: no such file or directory, open \'(.*)\'", file_not_found),
    (r"\[Error: ENOENT: no such file or directory, stat \'(.*)\'\] \{", file_not_found),
    (r'(.*):[0-9]+: error: Libtool library used but \'LIBTOOL\' is undefined',
     lambda m: MissingLibtool()),
    # libtoolize
    (r"libtoolize:   error: \'(.*)\' does not exist.", file_not_found),
    # Seen in python-cogent
    (
        "RuntimeError: Numpy required but not found.",
        lambda m: MissingPythonModule("numpy"),
    ),
    # Seen in cpl-plugin-giraf
    (
        r"ImportError: Numpy version (.*) or later must be " r"installed to use .*",
        lambda m: MissingPythonModule("numpy", minimum_version=m.group(1)),
    ),
    # Seen in mayavi2
    (
        r'\w+Numpy is required to build.*',
        lambda m: MissingPythonModule("numpy")
    ),
    # autoconf
    (r"configure.ac:[0-9]+: error: required file \'(.*)\' not found", file_not_found),
    # automake
    (r"Makefile.am: error: required file \'(.*)\' not found", file_not_found),
    # sphinx
    (r"config directory doesn\'t contain a conf.py file \((.*)\)", None),
    # vcversioner
    (
        r"vcversioner: no VCS could be detected in \'/<<PKGBUILDDIR>>\' "
        r"and \'/<<PKGBUILDDIR>>/version.txt\' isn\'t present.",
        None,
    ),
    # rst2html (and other Python?)
    (r"  InputError: \[Errno 2\] No such file or directory: \'(.*)\'", file_not_found),
    # gpg
    (r"gpg: can\'t connect to the agent: File name too long", None),
    (r"(.*.lua):[0-9]+: assertion failed", None),
    (r"\*\*\* error: gettext infrastructure mismatch: .*", None),
    (r"\s+\^\-\-\-\-\^ SC[0-4][0-9][0-9][0-9]: .*", None),
    (
        r"Error: (.*) needs updating from (.*)\. "
        r"Run \'pg_buildext updatecontrol\'.",
        need_pg_buildext_updatecontrol,
    ),
    (r"Patch (.*) does not apply \(enforce with -f\)", None),
    (
        r"convert convert: Unable to read font \((.*)\) "
        r"\[No such file or directory\].",
        file_not_found,
    ),
    (
        r"java.io.FileNotFoundException: (.*) \(No such file or directory\)",
        file_not_found,
    ),
    # Pytest
    (r"INTERNALERROR> PluginValidationError: (.*)", None),
    (r"[0-9]+ out of [0-9]+ hunks FAILED -- saving rejects to file (.*\.rej)", None),
    (r"pkg_resources.UnknownExtra: (.*) has no such extra feature \'(.*)\'", None),
    (
        r"dh_auto_configure: invalid or non-existing path "
        r"to the source directory: .*",
        None,
    ),
    # Sphinx
    (
        r"sphinx_rtd_theme is no longer a hard dependency since version (.*). "
        r"Please install it manually.\(pip install (.*)\)",
        lambda m: MissingPythonModule("sphinx_rtd_theme"),
    ),
    (r"There is a syntax error in your configuration file: (.*)", None),
    (
        r"E: The Debian version (.*) cannot be used as an ELPA version.",
        debian_version_rejected,
    ),
    (r'"(.*)" is not exported by the ExtUtils::MakeMaker module', None),
    (
        r"E: Please add appropriate interpreter package to Build-Depends, "
        r"see pybuild\(1\) for details\..*",
        dh_missing_addon,
    ),
    (r"dpkg: error: .*: No space left on device", lambda m: NoSpaceOnDevice()),
    (
        r"You need the GNU readline library(ftp://ftp.gnu.org/gnu/readline/ ) "
        r"to build",
        lambda m: MissingLibrary("readline"),
    ),
    HaskellMissingDependencyMatcher(),
    SetupPyCommandMissingMatcher(),
    CMakeErrorMatcher(),
    (
        r"error: failed to select a version for the requirement `(.*)`",
        cargo_missing_requirement,
    ),
    (r"^Environment variable \$SOURCE_DATE_EPOCH: No digits were found: $", None),
    (r'\[ERROR\] LazyFont - Failed to read font file (.*) '
     r'\<java.io.FileNotFoundException: (.*) \(No such file or directory\)\>'
     r'java.io.FileNotFoundException: (.*) \(No such file or directory\)',
     missing_lazyfont_file,
     ),
    (r'Package (.*) was not found in the pkg-config search path.',
     lambda m: MissingPkgConfig(m.group(1))),
    (r'go runtime is required: https://golang.org/doc/install',
     lambda m: MissingGoRuntime()),
    (r"\%Error: '(.*)' must be installed to build",
     lambda m: MissingCommand(m.group(1))),
    (r'configure: error: "Could not find (.*) in PATH"',
     lambda m: MissingCommand(m.group(1))),
    (r"go: .*: Get \"(.*)\": x509: certificate signed by unknown authority",
     lambda m: UnknownCertificateAuthority(m.group(1))),
    (r"\t\(Do you need to predeclare (.*)\?\)",
     lambda m: MissingPerlPredeclared(m.group(1))),
    (r"  vignette builder 'knitr' not found",
     lambda m: MissingRPackage('knitr')),
    (r'fatal: unable to auto-detect email address \(got \'.*\'\)',
     lambda m: MissingGitIdentity()),
    (r"gpg: no default secret key: No secret key",
     lambda m: MissingSecretGpgKey()),
    (r'ERROR: FAILED--Further testing stopped: '
     r'Test requires module \'(.*)\' but it\'s not found',
     lambda m: MissingPerlModule(None, m.group(1))),
    (r'(subprocess.CalledProcessError|error): '
     r'Command \'\[\'/usr/bin/python([0-9.]*)\', \'-m\', \'pip\', '
     r'\'--disable-pip-version-check\', \'wheel\', \'--no-deps\', \'-w\', '
     r'.*, \'([^-][^\']+)\'\]\' '
     r'returned non-zero exit status 1.',
     lambda m: MissingPythonDistribution.from_requirement_str(
         m.group(3),
         python_version=(int(m.group(2)[0]) if m.group(2) else None))
     ),
    (r'vcversioner: \[\'git\', .*, \'describe\', \'--tags\', \'--long\'\] '
     r'failed and \'(.*)/version.txt\' isn\'t present\.',
     lambda m: MissingVcVersionerVersion()),

    (r'# Module \'(.*)\' is not installed',
     lambda m: MissingPerlModule(None, m.group(1)),
     ),

    (
        r'configure: error: Missing lib(.*)\.',
        lambda m: MissingLibrary(m.group(1)),
    ),

    # Intentionally at the bottom of the list.
    (
        r'configure: error: Please install (.*) from (http:\/\/[^ ]+)',
        lambda m: MissingVagueDependency(m.group(1), url=m.group(2)),
    ),
    (
        r'configure: error: Required package (.*) is not available\.',
        lambda m: MissingVagueDependency(m.group(1)),
    ),
    (
        r'Error\! You need to have (.*) \((.*)\) around.',
        lambda m: MissingVagueDependency(m.group(1), url=m.group(2)),
    ),
    (
        r'configure: error: You don\'t have (.*) installed',
        lambda m: MissingVagueDependency(m.group(1))
    ),
    (
        r'configure: error: Could not find a recent version of (.*)',
        lambda m: MissingVagueDependency(m.group(1)),
    ),
    (
        r'configure: error: Unable to locate (.*)',
        lambda m: MissingVagueDependency(m.group(1)),
    ),
    (
        r'configure: error: Missing the (.*) library',
        lambda m: MissingVagueDependency(m.group(1)),
    ),
    (
        r'configure: error: Missing (.*)\.',
        lambda m: MissingVagueDependency(m.group(1)),
    ),
    (
        r'configure: error: Unable to find (.*), please install (.*)',
        lambda m: MissingVagueDependency(m.group(2)),
    ),
]


compiled_build_failure_regexps = []
for entry in build_failure_regexps:
    try:
        matcher: Matcher
        if isinstance(entry, tuple):
            (regexp, cb) = entry
            matcher = SingleLineMatcher(regexp, cb)
        else:
            matcher = entry  # type: ignore
        compiled_build_failure_regexps.append(matcher)
    except re.error as e:
        raise Exception("Error in %s: %s" % (regexp, e))


# Regexps that hint at an error of some sort, but not the error itself.
secondary_build_failure_regexps = [
    # Java
    r'Exception in thread "(.*)" (.*): (.*);',
    r"error: Unrecognized option: \'.*\'",
    r".*: No space left on device",
    r"Segmentation fault",
    r'make\[[0-9]+\]: (.*): No such file or directory',
    r"make\[[0-9]+\]: \*\*\* \[.*:[0-9]+: .*\] Segmentation fault",
    (
        r"make\[[0-9]+\]: \*\*\* No rule to make target "
        r"\'(?!maintainer-clean)(?!clean)(.*)\'\.  Stop\."
    ),
    r".*:[0-9]+: \*\*\* empty variable name.  Stop.",
    # QMake
    r"Project ERROR: .*",
    # pdflatex
    r"\!  ==> Fatal error occurred, no output PDF file produced\!",
    # latex
    r"\! Undefined control sequence\.",
    r"\! Emergency stop\.",
    r"\!pdfTeX error: pdflatex: fwrite\(\) failed",
    # inkscape
    r"Unknown option .*",
    # CTest
    r"Errors while running CTest",
    r"dh_auto_install: error: .*",
    r"dh.*: Aborting due to earlier error",
    r"dh.*: unknown option or error during option parsing; aborting",
    r"Could not import extension .* \(exception: .*\)",
    r"configure.ac:[0-9]+: error: (.*)",
    r"dwz: Too few files for multifile optimization",
    r"dh_dwz: dwz -q -- .* returned exit code [0-9]+",
    r"help2man: can\'t get `-?-help\' info from .*",
    r"[^:]+: line [0-9]+:\s+[0-9]+ Segmentation fault.*",
    r".*(No space left on device).*",
    r"dpkg-gencontrol: error: (.*)",
    r".*:[0-9]+:[0-9]+: (error|ERROR): (.*)",
    r"FAIL: (.*)",
    r"FAIL (.*) \(.*\)",
    r"FAIL\s+(.*) \[.*\] ?",
    r"TEST FAILURE",
    r"make\[[0-9]+\]: \*\*\* \[.*\] Error [0-9]+",
    r"make\[[0-9]+\]: \*\*\* \[.*\] Aborted",
    r"E: pybuild pybuild:[0-9]+: test: plugin [^ ]+ failed with:"
    r"exit code=[0-9]+: .*",
    r"chmod: cannot access \'.*\': No such file or directory",
    r"dh_autoreconf: autoreconf .* returned exit code [0-9]+",
    r"make: \*\*\* \[.*\] Error [0-9]+",
    r".*:[0-9]+: \*\*\* missing separator\.  Stop\.",
    r"[^:]+: cannot stat \'.*\': No such file or directory",
    r"[0-9]+ tests: [0-9]+ ok, [0-9]+ failure\(s\), [0-9]+ test\(s\) skipped",
    r"\*\*Error:\*\* (.*)",
    r"^Error: (.*)",
    r"Failed [0-9]+ tests? out of [0-9]+, [0-9.]+% okay.",
    r"Failed [0-9]+\/[0-9]+ test programs. [0-9]+/[0-9]+ subtests failed.",
    r"Original error was: (.*)",
    r"[^:]+: error: (.*)",
    r"[^:]+:[0-9]+: error: (.*)",
    r"[^:]+:[0-9]+:[0-9]+: error: (.*)",
    r"^FAILED \(.*\)",
    r"cat: (.*): No such file or directory",
    # Random Python errors
    "^(E  +)?(SyntaxError|TypeError|ValueError|AttributeError|NameError|"
    r"django.core.exceptions..*|RuntimeError|subprocess.CalledProcessError|"
    r"testtools.matchers._impl.MismatchError|"
    r"PermissionError|IndexError|TypeError|AssertionError|IOError|ImportError|"
    r"SerialException|OSError|qtawesome.iconic_font.FontError|"
    "redis.exceptions.ConnectionError|builtins.OverflowError|ArgumentError|"
    "httptools.parser.errors.HttpParserInvalidURLError|HypothesisException|"
    "SSLError|KeyError|Exception|rnc2rng.parser.ParseError|"
    "pkg_resources.UnknownExtra|tarfile.ReadError|"
    "numpydoc.docscrape.ParseError|"
    "datalad.support.exceptions.IncompleteResultsError"
    r"): .*",
    "^E   DeprecationWarning: .*",
    "^E       fixture '(.*)' not found",
    # Rake
    r"[0-9]+ runs, [0-9]+ assertions, [0-9]+ failures, [0-9]+ errors, " r"[0-9]+ skips",
    # Node
    r"# failed [0-9]+ of [0-9]+ tests",
    # Pytest
    r"(.*).py:[0-9]+: AssertionError",
    # Perl
    r"  Failed tests:  [0-9-]+",
    # Go
    "FAIL\t(.*)\t[0-9.]+s",
    r".*.go:[0-9]+:[0-9]+: (?!note:).*",
    r"can\'t load package: package \.: no Go files in /<<PKGBUILDDIR>>/(.*)",
    # Ld
    r"\/usr\/bin\/ld: cannot open output file (.*): No such file or directory",
    r"configure: error: (.*)",
    r"config.status: error: (.*)",
    r"E: Build killed with signal TERM after ([0-9]+) minutes of inactivity",
    r"    \[javac\] [^: ]+:[0-9]+: error: (.*)",
    r"1\) TestChannelFeature: ([^:]+):([0-9]+): assert failed",
    r"cp: target \'(.*)\' is not a directory",
    r"cp: cannot create regular file \'(.*)\': No such file or directory",
    r"couldn\'t determine home directory at (.*)",
    r"ln: failed to create symbolic link \'(.*)\': File exists",
    r"ln: failed to create symbolic link \'(.*)\': No such file or directory",
    r"ln: failed to create symbolic link \'(.*)\': Permission denied",
    r"ln: invalid option -- .*",
    r"mkdir: cannot create directory ‘(.*)’: No such file or directory",
    r"mkdir: cannot create directory ‘(.*)’: File exists",
    r"mkdir: missing operand",
    r"Fatal error: .*",
    "Fatal Error: (.*)",
    r'ERROR: Test "(.*)" failed. Exiting.',
    # scons
    r"ERROR: test\(s\) failed in (.*)",
    r"./configure: line [0-9]+: syntax error near unexpected token `.*\'",
    r"scons: \*\*\* \[.*\] ValueError : unsupported pickle protocol: .*",
    # yarn
    r"ERROR: There are no scenarios; must have at least one.",
    # perl
    r"Execution of (.*) aborted due to compilation errors.",
    r"ls: cannot access \'(.*)\': No such file or directory",
    r"Problem opening (.*): No such file or directory at (.*) line ([0-9]+)\.",
    # Mocha
    r"     AssertionError \[ERR_ASSERTION\]: Missing expected exception.",
    # lt (C++)
    r".*: .*:[0-9]+: .*: Assertion `.*\' failed.",
    r"(.*).xml: FAILED:",
    # ninja
    r"ninja: build stopped: subcommand failed.",
    r".*\.s:[0-9]+: Error: .*",
    # rollup
    r"\[\!\] Error: Unexpected token",
    # glib
    r"\(.*:[0-9]+\): [a-zA-Z0-9]+-CRITICAL \*\*: [0-9:.]+: .*",
    r"tar: option requires an argument -- \'.\'",
    r"tar: .*: Cannot stat: No such file or directory",
    # rsvg-convert
    r"Could not render file (.*.svg)",
    # pybuild tests
    r"ERROR: file not found: (.*)",
    # msgfmt
    r"/usr/bin/msgfmt: found [0-9]+ fatal errors",
    # Docker
    r"Cannot connect to the Docker daemon at "
    r"unix:///var/run/docker.sock. Is the docker daemon running\?",
    r"dh_makeshlibs: failing due to earlier errors",
    # Ruby
    r"([^:]+)\.rb:[0-9]+:in `([^\'])+\': (.*) \((.*)\)",
    r".*: \*\*\* ERROR: "
    r"There where errors/warnings in server logs after running test cases.",
    r"Errno::EEXIST: File exists @ dir_s_mkdir - .*",
    r"Test environment was found to be incomplete at configuration time,",
    r"libtool:   error: cannot find the library \'(.*)\' or "
    r"unhandled argument \'(.*)\'",
    r"npm ERR\! (.*)",
    r"install: failed to access \'(.*)\': (.*)",
    r"MSBUILD: error MSBUILD[0-9]+: Project file \'(.*)\' not found.",
    r"E: (.*)",
    r"(.*)\(([0-9]+),([0-9]+)\): Error: .*",
    # C #
    r"(.*)\.cs\([0-9]+,[0-9]+\): error CS[0-9]+: .*",
    r".*Segmentation fault.*",
    r"a2x: ERROR: (.*) returned non-zero exit status ([0-9]+)",
    r"-- Configuring incomplete, errors occurred\!",
    r'Error opening link script "(.*)"',
    r"cc: error: (.*)",
    r"\[ERROR\] .*",
    r"dh_auto_(test|build): error: (.*)",
    r'tar: This does not look like a tar archive',
]

compiled_secondary_build_failure_regexps = [
    re.compile(regexp) for regexp in secondary_build_failure_regexps
]


def find_build_failure_description(  # noqa: C901
    lines: List[str],
) -> Tuple[Optional[SingleLineMatch], Optional["Problem"]]:
    """Find the key failure line in build output.

    Returns:
      tuple with (match object, error object)
    """
    OFFSET = 250
    # Is this cmake-specific, or rather just kf5 / qmake ?
    cmake = False
    # We search backwards for clear errors.
    for i in range(1, OFFSET):
        lineno = len(lines) - i
        if lineno < 0:
            break
        if "cmake" in lines[lineno]:
            cmake = True
        for matcher in compiled_build_failure_regexps:
            linenos, err = matcher.match(lines, lineno)
            if linenos:
                lineno = linenos[-1]  # For now
                return SingleLineMatch.from_lines(lines, lineno), err

    # TODO(jelmer): Remove this in favour of CMakeErrorMatcher above.
    if cmake:
        missing_file_pat = re.compile(
            r"\s*The imported target \"(.*)\" references the file"
        )
        conf_file_pat = re.compile(
            r'\s*Could not find a configuration file for package "(.*)".*'
        )
        binary_pat = re.compile(r"  Could NOT find (.*) \(missing: .*\)")
        cmake_files_pat = re.compile(
            "^  Could not find a package configuration file provided "
            'by "(.*)" with any of the following names:'
        )
        # Urgh, multi-line regexes---
        for lineno in range(len(lines)):
            line = lines[lineno].rstrip("\n")
            m = re.fullmatch(binary_pat, line)
            if m:
                return (
                    SingleLineMatch.from_lines(lines, lineno),
                    MissingCommand(m.group(1).lower()))
            m = re.fullmatch(missing_file_pat, line)
            if m:
                lineno += 1
                while lineno < len(lines) and not line:
                    lineno += 1
                if lines[lineno + 2].startswith("  but this file does not exist."):
                    m = re.fullmatch(r'\s*"(.*)"', line)
                    if m:
                        filename = m.group(1)
                    else:
                        filename = line
                    return (
                        SingleLineMatch.from_lines(lines, lineno),
                        MissingFile(filename))
                continue
            m = re.fullmatch(conf_file_pat, line)
            if m:
                package = m.group(1)
                m = re.match(
                    r'.*requested version "(.*)"\.', lines[lineno + 1].rstrip("\n")
                )
                if not m:
                    logger.warn("expected version string in line %r", lines[lineno + 1])
                    continue
                version = m.group(1)
                return (
                    SingleLineMatch.from_lines(lines, lineno),
                    MissingPkgConfig(package, version))
            if lineno + 1 < len(lines):
                m = re.fullmatch(
                    cmake_files_pat,
                    line
                    + " "
                    + lines[lineno + 1].lstrip(" ").strip("\n"),
                )
                if m and lines[lineno + 2] == "\n":
                    i = 3
                    filenames = []
                    while lines[lineno + i].strip():
                        filenames.append(lines[lineno + i].strip())
                        i += 1
                    return (
                        SingleLineMatch.from_lines(lines, lineno),
                        CMakeFilesMissing(filenames))

    # And forwards for vague ("secondary") errors.
    for lineno in range(max(0, len(lines) - OFFSET), len(lines)):
        line = lines[lineno].strip("\n")
        for regexp in compiled_secondary_build_failure_regexps:
            m = regexp.fullmatch(line)
            if m:
                return SingleLineMatch.from_lines(lines, lineno), None
    return None, None


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser("analyse-build-log")
    parser.add_argument("path", type=str)
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format='%(message)s')

    with open(args.path, "r") as f:
        lines = f.readlines()

    m, problem = find_build_failure_description(lines)

    if not m:
        logging.info('No issues found')
    else:
        logging.info('Issue found at line %d:', m.lineno)
        logging.info('%s', m.line)

    if problem:
        logging.info('Identified issue: %s: %s', problem.kind, problem)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))
