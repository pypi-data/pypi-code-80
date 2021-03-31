# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['lbfi']
entry_points = \
{'console_scripts': ['lbfi = lbfi:cli']}

setup_kwargs = {
    'name': 'lbfi',
    'version': '0.1.2',
    'description': 'lbfi stands for Linux Bangla Font Installer. You can avail the fonts for your linux desktop easily with this tool.',
    'long_description': None,
    'author': 'fahadahammed',
    'author_email': 'iamfahadahammed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
