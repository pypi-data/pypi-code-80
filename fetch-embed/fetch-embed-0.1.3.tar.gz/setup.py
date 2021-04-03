# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fetch_embed']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=1.6.2,<2.0.0',
 'httpx>=0.17.1,<0.18.0',
 'logzero>=1.7.0,<2.0.0',
 'numpy>=1.20.2,<2.0.0']

setup_kwargs = {
    'name': 'fetch-embed',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'freemt',
    'author_email': 'yucongo+fmt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
