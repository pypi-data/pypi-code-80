#!/usr/bin/env python

from setuptools import find_packages
from distutils.core import setup

entry_points = {
    "console_scripts": [
        "zanza = zanza.__main__:main",
        "dezanza = dezanza.__main__:main"
    ]
}

setup(
    name="zanza",
    version="0.1.0",
    author="fogasl",
    description="Dead-simple string obfuscation library",
    long_description=open("README.md", "r", encoding="utf8").read(),
    long_description_content_type="text/markdown",
    keywords="simple string obfuscation",
    license="BSD-3-Clause",
    python_requires=">3",
    packages=find_packages(),
    entry_points=entry_points
)
