# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['researchhelper']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.0,<4.0.0', 'numpy>=1.20.1,<2.0.0', 'scipy>=1.6.2,<2.0.0']

setup_kwargs = {
    'name': 'researchhelper',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Bas Chatel',
    'author_email': 'bastiaan.chatel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
