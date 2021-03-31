# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lwh']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['lwh = lwh.main:app']}

setup_kwargs = {
    'name': 'lwh',
    'version': '0.0.11',
    'description': 'Lacework Helios Project cli',
    'long_description': '',
    'author': 'jeffthorne',
    'author_email': 'jthorne@u.washington.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
