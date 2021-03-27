#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os

exec(open('shear_bias/info.py').read())

def readme():
    with open('README.rst') as f:
        return f.read()

home = os.environ['HOME']

setup(name = __whoami__,
      author = __author__,
      packages = [__whoami__],
      version = __version__,
      description = 'Shear bias estimation tools',
      long_description = readme(),
      url = 'https://github.com/cosmostat/shear_bias',
      author_email = __email__,
      platforms = ['posix', 'mac os'],
      license = "GNU GPLv3",
      classifiers = [
                     'Programming Language :: Python',
                     'Natural Language :: English',
                    ],
)


