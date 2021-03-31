# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makru_langc_new']

package_data = \
{'': ['*']}

install_requires = \
['clint>=0.5.1,<0.6.0', 'makru>=0.1.0-rc.3,<0.2.0']

entry_points = \
{'console_scripts': ['makru_langc_new = makru_langc_new:main']}

setup_kwargs = {
    'name': 'makru-langc-new',
    'version': '0.1.0a1',
    'description': 'a mini program to create directory layout for c project using makru_langc',
    'long_description': None,
    'author': 'thisLight',
    'author_email': 'l1589002388@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
