__all__ = [
    "Extension",
    "Library"
]

from typing import Optional
from perfting.setuptools.attriclass import attriclass

class Extension(attriclass(
        name = "name",
        sources = "sources",
        include = "include_dirs",
        macros = None,
        library = None,
        extra = None,
        symbols = "export_symbols",
        depends = "depends",
        language = "language",
        optional = "optional")):

    class Macros(attriclass(
            define = "define_macros",
            undef = "undef_macros")):

        def __init__(self, *,
                define: Optional[list[tuple[str, Optional[str]]]] = None,
                undef: Optional[list[str]] = None) -> None:
            self.define = define
            self.undef = undef

    class Library(attriclass(
            directorys = "library_dirs",
            libraries = "libraries",
            runtime = "runtime_library_dirs")):

        def __init__(self, *,
                directorys: Optional[list[str]] = None,
                libraries: Optional[list[str]] = None,
                runtimes: Optional[list[str]] = None) -> None:
            self.directorys = directorys
            self.libraries = libraries
            self.runtimes = runtimes

    class Extra(attriclass(
            objects = "extra_objects",
            compile_args = "extra_compile_args",
            link_args = "extra_link_args")):

        def __init__(self, *,
                objects: Optional[list[str]] = None,
                compile_args: Optional[list[str]] = None,
                link_args: Optional[list[str]] = None) -> None:
            self.objects = objects
            self.compile_args = compile_args
            self.link_args = link_args

    def __init__(self, *,
            name: str,
            sources: list[str],
            include: Optional[list[str]] = None,
            macros: Optional[Macros] = None,
            library: Optional[Library] = None,
            extra: Optional[Extra] = None,
            symbols: Optional[list[str]] = None,
            depends: Optional[list[str]] = None,
            language: Optional[str] = None,
            optional: Optional[str] = None) -> None:
        self.name = name
        self.sources = sources
        self.include = include
        self.macros = macros
        self.library = library
        self.extra = extra
        self.symbols = symbols
        self.depends = depends
        self.language = language
        self.optional = optional

class Library(Extension): ...