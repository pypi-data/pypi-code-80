# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kindlenotes2md']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyquery>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['kindlenotes2md = kindlenotes2md.notes:cli']}

setup_kwargs = {
    'name': 'kindlenotes2md',
    'version': '0.1.1',
    'description': 'Convert your kindle notes to markdown format',
    'long_description': None,
    'author': 'Ewan Nicolson',
    'author_email': 'ewan.nicolson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dataewan/kindlenotes2md',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
