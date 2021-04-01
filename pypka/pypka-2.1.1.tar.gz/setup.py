# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypka',
 'pypka.CHARMM36m',
 'pypka.G54A7',
 'pypka.clean',
 'pypka.clean.pdb2pqr',
 'pypka.clean.pdb2pqr.conf_avg',
 'pypka.clean.pdb2pqr.extensions',
 'pypka.clean.pdb2pqr.src',
 'pypka.delphi4py',
 'pypka.delphi4py.example',
 'pypka.delphi4py.readFiles',
 'pypka.delphi4py.rundelphi',
 'pypka.mc']

package_data = \
{'': ['*'],
 'pypka.CHARMM36m': ['sts/*'],
 'pypka.G54A7': ['sts/*', 'sts_old/*'],
 'pypka.clean.pdb2pqr': ['dat/*', 'tools/*']}

install_requires = \
['numpy', 'psutil']

setup_kwargs = {
    'name': 'pypka',
    'version': '2.1.1',
    'description': 'A python module for flexible Poisson-Boltzmann based pKa calculations with proton tautomerism',
    'long_description': None,
    'author': 'Pedro Reis',
    'author_email': 'pdreis@fc.ul.pt',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
