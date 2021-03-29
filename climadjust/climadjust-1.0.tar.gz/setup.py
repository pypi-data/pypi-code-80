#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='climadjust',
    platforms=['GNU/Linux'],
    version='1.0',
    author='Predictia',
    description="Python client for Climadjust API",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['climadjust', 'climadjust.clientMethods', 'climadjust.DTOs'],
    install_requires=['requests',
                      'tenacity',
                      'shapely',
                      'ciso8601'
                      ],
    include_package_data=True
)
