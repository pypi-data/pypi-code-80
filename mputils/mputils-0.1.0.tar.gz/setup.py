# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mputils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mputils = mputils.cli:app']}

setup_kwargs = {
    'name': 'mputils',
    'version': '0.1.0',
    'description': 'Multiprocessing move/copy',
    'long_description': None,
    'author': 'Panos Mavrogiorgos',
    'author_email': 'pmav99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
