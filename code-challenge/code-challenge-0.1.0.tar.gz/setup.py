# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_challenge']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'firebase>=3.0.1,<4.0.0']

entry_points = \
{'console_scripts': ['coding-interview = main:main']}

setup_kwargs = {
    'name': 'code-challenge',
    'version': '0.1.0',
    'description': 'Coding interview CLI that directs the user to answer timed coding interview questions in Python, JS, or C++',
    'long_description': None,
    'author': 'Andrew Peng',
    'author_email': 'andrewpeng02@Gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
