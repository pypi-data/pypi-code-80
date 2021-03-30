# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfssl_cli', 'cfssl_cli.test']

package_data = \
{'': ['*'], 'cfssl_cli': ['config/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'cfssl>=0.0.3-beta.243,<0.0.4',
 'click>=7.1.2,<8.0.0',
 'cryptography>=3.4.7,<4.0.0']

entry_points = \
{'console_scripts': ['cfssl-cli = cfssl_cli.__main__:main']}

setup_kwargs = {
    'name': 'cfssl-cli',
    'version': '1.4.0',
    'description': 'This CLI tool allows you to generate certificates from a remote CFSSL server.',
    'long_description': None,
    'author': 'Rémi Alvergnat',
    'author_email': 'toilal.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Toilal/python-cfssl-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
