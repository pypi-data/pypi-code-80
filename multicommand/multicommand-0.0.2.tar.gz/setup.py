# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['multicommand']
setup_kwargs = {
    'name': 'multicommand',
    'version': '0.0.2',
    'description': 'Create simple nested argparse CLIs',
    'long_description': None,
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
