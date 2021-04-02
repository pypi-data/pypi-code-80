# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qset_tslib',
 'qset_tslib.cython',
 'qset_tslib.cython.neutralize',
 'qset_tslib.models',
 'qset_tslib.technical_indicators']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.3,<2.0.0',
 'scikit-learn>=0.23.1,<0.24.0',
 'scipy>=1.6.2,<2.0.0',
 'statsmodels>=0.12.2,<0.13.0']

setup_kwargs = {
    'name': 'qset-tslib',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Arsenii Kadaner',
    'author_email': 'arseniikadaner@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
