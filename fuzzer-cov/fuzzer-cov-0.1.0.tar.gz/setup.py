#!/usr/bin/env python
import os
from setuptools import setup

with open('README.md', 'r') as f:
    readme_content = f.read()

setup(
    name='fuzzer-cov',
    version='0.1.0',
    long_description=readme_content,
    long_description_content_type='text/markdown',
    url='https://github.com/Myriad-Dreamin/fuzzer-cov',
    download_url='https://github.com/Myriad-Dreamin/fuzzer-cov/archive/v0.1.0.tar.gz',
    author='Myriad Dreamin',
    author_email='camiyoru@gmail.com',
    license='MIT',
    packages=['fuzzer-cov'],
    install_requires=[],
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ]
)