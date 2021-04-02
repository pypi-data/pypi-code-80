# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['multicommand']
setup_kwargs = {
    'name': 'multicommand',
    'version': '0.0.3',
    'description': 'Simple subcommand CLIs with argparse',
    'long_description': None,
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewrosss/multicommand',
    'py_modules': modules,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
