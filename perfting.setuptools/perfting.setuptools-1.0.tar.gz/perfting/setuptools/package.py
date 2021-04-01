__all__ = [
    "Packages"
]

from typing import Optional
from perfting.setuptools.attriclass import attriclass
import setuptools # type: ignore

class Package(attriclass(
        name = "name",
        version = "version",
        description = None,
        license = "license",
        url = None,
        author = None,
        maintainer = None,
        packages = None,
        requires = None,
        entry = "entry_points",
        zip = "zip_safe")):


    class Author(attriclass(
            name = "author",
            mail = "author_email")):

        def __init__(self, *,
                name: Optional[str] = None,
                mail: Optional[str] = None) -> None:
            self.name = name
            self.mail = mail

    class Maintainer(attriclass(
            name = "maintainer",
            mail = "maintainer_email")):

        def __init__(self, *,
                name: Optional[str] = None,
                mail: Optional[str] = None) -> None:
            self.name = name
            self.mail = mail

    class Description(attriclass(
            short = "description",
            long = "long_description")):

        def __init__(self,
                short: Optional[str] = None, *,
                long: Optional[str] = None) -> None:
            self.short = short
            self.long = long

    class URL(attriclass(
            home = "url",
            download = "download_url",
            urls = "project_urls")):

        def __init__(self,
                home: Optional[str] = None,
                download: Optional[str] = None,
                urls: Optional[dict[str, str]] = None) -> None:
            self.home = home
            self.download = download
            self.urls = urls

    class Packages(attriclass(
            packages = "packages",
            data = "package_data",
            directory = "package_dir",
            namespaces = "namespace_packages")):

        def __init__(self,
                *packages: str,
                data: Optional[dict[str, list[str]]] = None,
                directory: Optional[dict[str, str]] = None,
                namespaces: Optional[list[str]] = None) -> None:
            self.packages = [*packages]
            self.data = data
            self.directory = directory
            self.namespaces = namespaces

    class Requires(attriclass(
            requires = "install_requires",
            extras = "extras_require",
            python = "python_requires")):

        def __init__(self,
                *requires: str,
                extras: Optional[dict[str, list[str]]] = None,
                python: Optional[str] = None) -> None:
            self.requires = requires
            self.extras = extras
            self.python = python

    def __init__(self, *,
            name: str,
            version: Optional[str] = None,
            description: Optional[Description] = None,
            license: Optional[str] = None,
            url: Optional[URL] = None,
            platforms: Optional[list[str]] = None,
            classifiers: Optional[list[str]] = None,
            author: Optional[Author] = None,
            maintainer: Optional[Maintainer] = None,
            packages: Optional[Packages] = None,
            requires: Optional[Requires] = None,
            entry: Optional[dict[str, list[str]]] = None,
            zip: bool = False) -> None:
        self.name = name
        self.version = version
        self.description = description
        self.license = license
        self.url = url
        self.platforms = platforms
        self.classifiers = classifiers
        self.author = author
        self.maintainer = maintainer
        self.packages = packages
        self.requires = requires
        self.entry = entry
        self.zip = zip

    def setup(self) -> None:
        setuptools.setup(**self.extract()) # type: ignore