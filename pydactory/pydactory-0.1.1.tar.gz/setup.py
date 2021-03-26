# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydactory']

package_data = \
{'': ['*']}

install_requires = \
['faker>=4.15.0,<5.0.0', 'pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'pydactory',
    'version': '0.1.1',
    'description': 'A factory library for pydantic models.',
    'long_description': None,
    'author': 'Richard Howard',
    'author_email': 'richard@howard.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
