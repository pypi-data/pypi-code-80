# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastel']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<0.64.0', 'revdb>=1.0.5,<2.0.0', 'revjwt>=1.0.4,<2.0.0']

setup_kwargs = {
    'name': 'fastel',
    'version': '1.0.7',
    'description': '',
    'long_description': None,
    'author': 'Chien',
    'author_email': 'a0186163@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
