#!/usr/bin/env python3
""" Setup script for this package"""

from distutils.core import setup
import os

## The text of the README file
readme_text = ""
if os.path.exists("README.md"):
    with open("README.md") as fh:
        readme_text = fh.read()

setup(
    name = 'multi-git',
    version = '0.1.4',
    description = 'Multi-Git',
    author = 'Daniel Kullmann',
    author_email = 'python@danielkullmann.de',
    url = '',
    packages = [],
    scripts = ['multi-git'],
    requires = ['toml', 'config_path'],
    license = "MIT",
    long_description=readme_text,
    long_description_content_type="text/markdown",
)
