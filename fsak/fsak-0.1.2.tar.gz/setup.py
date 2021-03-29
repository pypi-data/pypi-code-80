# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fsak']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['fsak = fsak.fsak:execute']}

setup_kwargs = {
    'name': 'fsak',
    'version': '0.1.2',
    'description': 'sak=swiss army knife',
    'long_description': None,
    'author': 'fahadahammed',
    'author_email': 'iamfahadahammed@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
