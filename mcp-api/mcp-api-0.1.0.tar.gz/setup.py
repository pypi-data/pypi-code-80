# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mcp-api']
install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'mcp-api',
    'version': '0.1.0',
    'description': 'A small unofficial Wrapper for the Minecraft game Profiles API.',
    'long_description': None,
    'author': 'Julheer',
    'author_email': 'admin0x12@julheer.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
