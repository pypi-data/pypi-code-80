# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cbpro']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=3.5.1,<4.0.0',
 'requests>=2.13.0,<3.0.0',
 'six>=1.10.0,<2.0.0',
 'sortedcontainers>=2.0,<3.0',
 'websocket-client>=0.40.0,<1.0.0']

setup_kwargs = {
    'name': 'coinbasepro-revived',
    'version': '1.1.10',
    'description': 'Revived https://github.com/danpaquin/coinbasepro-python. Python package to interact with the coinbase pro api https://docs.pro.coinbase.com/.',
    'long_description': None,
    'author': 'me',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
