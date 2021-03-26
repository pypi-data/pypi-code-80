#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

install_requires = \
['pytest>=5.0.0']

entry_points = \
{'pytest11': ['srcpaths = pytest_yuk']}

setup(name='pytest-yuk',
      version='0.0.1.post2',
      description='Display tests you are uneasy with, using 🤢/🤮 for pass/fail of tests marked with yuk.',
      author='Brian Okken',
      author_email='brian+pypi@pythontest.com',
      url='https://github.com/okken/pytest-yuk',
      py_modules=['pytest_yuk'],
      install_requires=install_requires,
      entry_points=entry_points,
     )
