# noinspection Mypy
from typing import List, Any

from setuptools import setup, find_packages
from os import path, getcwd

# from https://packaging.python.org/tutorials/packaging-projects/

# noinspection SpellCheckingInspection
package_name = "helix.fhir.client.sdk"

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    with open(path.join(getcwd(), "VERSION")) as version_file:
        version = version_file.read().strip()
except IOError:
    raise


def fix_setuptools() -> None:
    """Work around bugs in setuptools.

    Some versions of setuptools are broken and raise SandboxViolation for normal
    operations in a virtualenv. We therefore disable the sandbox to avoid these
    issues.
    """
    try:
        from setuptools.sandbox import DirectorySandbox

        # noinspection PyUnusedLocal
        def violation(operation: Any, *args: Any, **_: Any) -> None:
            print("SandboxViolation: %s" % (args,))

        DirectorySandbox._violation = violation
    except ImportError:
        pass


# Fix bugs in setuptools.
fix_setuptools()


def parse_requirements(file: str) -> List[str]:
    with open(file, "r") as fs:
        return [
            r
            for r in fs.read().splitlines()
            if (
                len(r.strip()) > 0
                and not r.strip().startswith("#")
                and not r.strip().startswith("--")
            )
        ]


# classifiers list is here: https://pypi.org/classifiers/

# create the package setup
setup(
    name=package_name,
    version=version,
    author="Julie",
    author_email="foo@email.com",
    description="helix.fhir.client.sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/icanbwell/helix.fhir.client.sdk",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    dependency_links=[],
    include_package_data=True,
    zip_safe=False,
    package_data={"helix.fhir.client.sdk": ["py.typed"]},
)
