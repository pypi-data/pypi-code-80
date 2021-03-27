import os
import re
import sys
import site
import json
import argparse
import platform
import configparser
from pathlib import Path
from contextlib import contextmanager

## Exceptions
from .pyckagelib.error import PyckageError, PyckageExit
from .pyckagelib import (
    PackageData,
    FileTree,
    FileTemplate,
    FileTracker,
    Validate,
)

__version__ = "0.1.1"

## To be used with the module
_PYCKAGE_DATA = PackageData("pyckage")


class PyckageValidate(Validate):
    """"""

    RE_FLAGS = re.UNICODE

    RE_AUTHOR = re.compile(r"[\S ]+", RE_FLAGS)
    RE_USER = re.compile(r"[a-zA-Z]+", RE_FLAGS)
    RE_EMAIL = re.compile(
        r"^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$",
        RE_FLAGS,
    )
    RE_VERSION = re.compile(
        r"^(0|[1-9]\d*)(\.(0|[1-9]\d*))(\.(0|[1-9]\d*))?$", RE_FLAGS
    )
    RE_PACKAGE = re.compile(r"^[a-zA-Z][a-zA-Z\_\-]+$", RE_FLAGS)
    RE_DESCRIPTION = re.compile(r"[\S\s]*", RE_FLAGS | re.MULTILINE)

    @classmethod
    def description(cls, description: str, null: bool = None) -> str:
        return cls._regex(cls.RE_DESCRIPTION, description, "description", null=null)

    @classmethod
    def author(cls, author: str, null: object = None) -> str:
        return cls._regex(cls.RE_AUTHOR, author, "author", null=null)

    @classmethod
    def user(cls, user: str, null: object = None) -> str:
        return cls._regex(cls.RE_AUTHOR, user, "user", null=null)

    @classmethod
    def email(cls, email: str, null: bool = None) -> str:
        return cls._regex(cls.RE_EMAIL, email, "email", null=null)

    @classmethod
    def version(cls, version: str, null: bool = False) -> str:
        return cls._regex(cls.RE_VERSION, version, "version", null=null)

    @classmethod
    def package(cls, package: str, null: bool = False) -> str:
        return cls._regex(cls.RE_PACKAGE, package, "package name", null=null)

    @classmethod
    def path(cls, path: str, null: bool = None) -> Path:
        if path is None and null is not False:
            return Path.cwd().absolute()
        elif type(path) is str or type(path) is Path:
            path = Path(path)
            if not path.exists():
                raise cls.Invalid(f"Path `{path}` not found.")
            else:
                return path.absolute()
        else:
            raise cls.Invalid(f"Invalid path type {type(path)}")

    @classmethod
    def platform(cls, platform_: str, null: bool = False) -> str:
        if platform_ is None and null is not False:
            return platform.system()
        elif type(platform_) is str:
            if platform_ in {"Windows", "Linux", "Darwin", "Java", "Solaris"}:
                return platform_
            else:
                raise cls.Invalid(f"Invalid platform {platform_}")
        else:
            raise cls.Invalid(f"Invalid platform type {type(platform_)}")


class PyckageTemplate(FileTemplate):
    """"""

    package_data = _PYCKAGE_DATA

    @FileTemplate.template("setup.cfg")
    def setupcfg(self, source: str, dest: str) -> str:
        cfg_files = ["setup-plain.cfg.t"]

        if self.get("args").data:
            cfg_files.append("setup-data.cfg.t")

        if self.get("args").script:
            cfg_files.append("setup-script.cfg.t")

        if self.get("args").github:
            cfg_files.append("setup-github.cfg.t")

        ## Parse all configuration templates.
        parser = configparser.ConfigParser()
        parser.read([self.package_data.get_data_path(fname) for fname in cfg_files])

        ## Summarise and write to file.
        with self.package_data.open_data("setup.cfg.t", mode="w") as file:
            parser.write(file)

        return (self.package_data.get_data_path("setup.cfg.t"), Path("setup.cfg"))


class Pyckage(object):
    """"""

    package_data = _PYCKAGE_DATA

    def __init__(
        self,
        *,
        description: str = None,
        package: str = None,
        pathlog: list = None,
        version: str = None,
        author: str = None,
        email: str = None,
        user: str = None,
        path: str = None,
        meta: dict = None,
    ):
        self.description = description
        self.package = package
        self.version = version
        self.author = author
        self.email = email
        self.user = user
        self.path = path
        self.meta = meta

        # Meta parameters
        self._pyckage_version = self.kwget("pyckage_version", self.meta, __version__)
        self._system_platform = self.kwget(
            "system_platform", self.meta, platform.system()
        )

        self._py_min = self.kwget(
            "py_min", self.meta, f"{sys.version_info.major}.{sys.version_info.minor}"
        )
        self._py_max = self.kwget("py_max", self.meta, f"{sys.version_info.major + 1}")

        self.validate()

        self.tracker = FileTracker(pathlog)

    @property
    def info(self) -> dict:
        return {
            ## External
            "package_data": self.package_data.package_data,
            ## Common
            "description": self.description,
            "package": self.package,
            "version": self.version,
            "author": self.author,
            "email": self.email,
            "user": self.user,
            ## Meta
            "py_min": self._py_min,
            "py_max": self._py_max,
        }

    @classmethod
    def kwget(cls, key: object, kwargs: dict, default: object = None):
        if kwargs is None or key not in kwargs:
            return default
        else:
            return kwargs[key]

    def validate(self):
        try:
            # description
            self.description = PyckageValidate.description(self.description)

            # package
            self.package = PyckageValidate.package(self.package)

            # version
            self.version = PyckageValidate.version(self.version)

            # author
            self.author = PyckageValidate.author(self.author)

            # email
            self.email = PyckageValidate.email(self.email)

            # user
            self.user = PyckageValidate.user(self.user)

            self.validate_meta()
        except PyckageValidate.Invalid as error:
            raise ValueError(*error.args)

    def validate_meta(self):
        """"""
        self._pyckage_version = PyckageValidate.version(self._pyckage_version)
        self._system_platform = PyckageValidate.platform(self._system_platform)

    @classmethod
    def load(cls, pyckage_path: str):
        path = Path(pyckage_path).joinpath(".pyckage").absolute()

        if not path.exists():
            raise FileNotFoundError(f"No Pyckage installed at `{pyckage_path}`.")

        with open(path, mode="r") as file:
            return cls.JSON_DECODE(file.read())

    def save(self):
        """"""
        if not self.path.exists():
            raise FileNotFoundError(
                f"Misleading pyckage installation for `{self.package}`. Try running `pyckage fix`."
            )

        path = self.path.joinpath(".pyckage")

        with open(path, mode="w") as file:
            return file.write(self.JSON_ENCODE())

    @classmethod
    def pack(cls, args: argparse.Namespace):
        """"""
        ## Get pyckage path
        path = PyckageValidate.path(args.path)

        if not path.exists():
            raise FileNotFoundError(f"No target directory `{path}`.")
        elif not path.is_dir():
            raise OSError(f"`{path}` is not a directory.")

        pyckage_path = path.joinpath(".pyckage")

        if pyckage_path.exists():
            raise FileExistsError(
                "There is an existing Pyckage in this folder. Try running `pyckage update` or `pyckage fix`"
            )

        package: str = args.package

        if package is None:
            package = path.stem

        version: str = args.version

        if version is None:
            version = "0.0.0"

        ## Get global config
        config = cls.package_data.get_config()

        author: str = args.author

        if author is None:
            author = config["author"]

        email: str = args.email

        if email is None:
            email = config["email"]

        user: str = args.user

        if user is None:
            user = config["user"]

        description: str = args.description

        pyckage = cls(
            package=package,
            version=version,
            author=author,
            email=email,
            user=user,
            path=path,
            description=description,
        )

        pyckage.tree(args=args).grow(pyckage.path, tracker=pyckage.tracker)

        return pyckage

    def JSON_ENCODE(self) -> str:
        """
        {
            'meta': {
                    'pyckage_version': '0.0.0',
                    'platform': 'windows',
                    'pathlog': ['c:/users/author/pyckage/*', ...],
                    'py_min': '3.7',
                    'py_max': '4',
                },
            'package': 'pyckage',
            'version': '1.0.0',
            'author': 'Author Smith',
            'email': 'author@email.net',
            'user': 'author1998',
            'path': 'c:/users/author/pyckage/',
            'description': 'This is clearly a Python Package'
        }
        """
        return json.dumps(
            {
                "meta": {
                    "pyckage_version": self._pyckage_version,
                    "system_platform": self._system_platform,
                    "py_min": self._py_min,
                    "py_max": self._py_max,
                },
                "description": self.description,
                "pathlog": [[type_, str(path)] for type_, path in self.tracker.pathlog],
                "package": self.package,
                "version": self.version,
                "author": self.author,
                "email": self.email,
                "user": self.user,
                "path": str(self.path),
            }
        )

    @classmethod
    def JSON_DECODE(cls, json_data: str):
        return cls(**json.loads(json_data))

    def clear(self):
        """"""
        self.tracker.clear()

    # Some Checks
    @classmethod
    def has_pyckage(cls, path: str) -> bool:
        return Path(path).joinpath(".pyckage").exists()

    @classmethod
    def exit(cls, code: int = 0, msg: str = ""):
        raise PyckageExit(code, msg)

    def tree(self, *, args: argparse.Namespace = None) -> FileTree:
        """"""
        if args is None:
            raise ValueError("`args` is None")
        else:
            PyckageTemplate.set(args=args)

        T = FileTree  # Alias

        return T.root(
            [
                T(
                    T.DIR,
                    "src",
                    [
                        T(
                            T.DIR,
                            self.package,
                            [
                                T(
                                    T.FILE,
                                    "__init__.py",
                                    template=PyckageTemplate(
                                        source=self.package_data.get_data_path(
                                            "__init__.py.t"
                                        ),
                                        info=self.info,
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                T(
                    T.DIR,
                    "bin",
                    [
                        T(
                            T.FILE,
                            self.package,
                            template=PyckageTemplate(
                                source=self.package_data.get_data_path("package.t"),
                                info=self.info,
                            ),
                        )
                    ],
                    cond=args.script,
                ),
                T(T.DIR, "docs", []),
                T(T.DIR, "data", [], cond=args.data),
                T(
                    T.FILE,
                    "setup.py",
                    template=PyckageTemplate(
                        source=self.package_data.get_data_path("setup.py.t"),
                        info=self.info,
                    ),
                ),
                T(
                    T.FILE,
                    "setup.cfg",
                    template=PyckageTemplate(
                        source=self.package_data.get_data_path("setup.cfg.t"),
                        info=self.info,
                        key="setup.cfg",
                    ),
                ),
                T(T.FILE, ".pyckage"),
            ]
        )