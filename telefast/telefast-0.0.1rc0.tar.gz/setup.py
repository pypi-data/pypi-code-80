# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['telefast']

package_data = \
{'': ['*']}

install_requires = \
['Telethon>=1.21.1,<2.0.0']

setup_kwargs = {
    'name': 'telefast',
    'version': '0.0.1rc0',
    'description': '',
    'long_description': None,
    'author': 'aahnik',
    'author_email': 'daw@aahnik.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
