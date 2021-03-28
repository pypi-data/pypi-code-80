# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neverlose',
 'neverlose.enums',
 'neverlose.exceptions',
 'neverlose.handlers',
 'neverlose.methods',
 'neverlose.models',
 'neverlose.models.base',
 'neverlose.models.events',
 'neverlose.models.responses',
 'neverlose.utils']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0',
 'pydantic>=1.8.1,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'uvicorn>=0.13.4,<0.14.0']

setup_kwargs = {
    'name': 'neverlose',
    'version': '1.0.0',
    'description': 'Neverlose web api wrapper',
    'long_description': None,
    'author': 'es3n1n',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
