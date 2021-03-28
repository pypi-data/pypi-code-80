# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['squiral']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'squiral',
    'version': '0.1.1',
    'description': 'squiral - square spiral',
    'long_description': '# squiral.py\n\n**squ**are sp**iral**\n\n```\nWelcome to Squiral!\nHere is an example:\n21 22 23 24 25\n20  7  8  9 10\n19  6  1  2 11\n18  5  4  3 12\n17 16 15 14 13\n',
    'author': 'SADIK KUZU',
    'author_email': 'sadikkuzu@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
