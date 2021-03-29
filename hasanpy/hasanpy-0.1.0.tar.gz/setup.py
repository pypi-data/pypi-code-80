# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hasanpy']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1,<8.0']

entry_points = \
{'console_scripts': ['hasanpy = hasanpy.__main__:main']}

setup_kwargs = {
    'name': 'hasanpy',
    'version': '0.1.0',
    'description': 'A Python implementation of the Chicken esoteric programming language, with Hasan as its only token',
    'long_description': None,
    'author': 'kosayoda',
    'author_email': 'mdibaiee@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mdibaiee/hasanpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
