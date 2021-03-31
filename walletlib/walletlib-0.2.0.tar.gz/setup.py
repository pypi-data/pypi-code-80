# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['walletlib', 'walletlib.scripts']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.17.0,<0.18.0',
 'base58>=2.1.0,<3.0.0',
 'bsddb3>=6.2.9,<7.0.0',
 'click>=7.1.2,<8.0.0',
 'coincurve>=13.0.0,<14.0.0',
 'pycryptodome>=3.9.8,<4.0.0']

entry_points = \
{'console_scripts': ['dumpwallet = walletlib.scripts.dumpwallet:main']}

setup_kwargs = {
    'name': 'walletlib',
    'version': '0.2.0',
    'description': 'Library for accessing cryptocurrency wallet files',
    'long_description': None,
    'author': 'jim zhou',
    'author_email': '43537315+jimtje@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
