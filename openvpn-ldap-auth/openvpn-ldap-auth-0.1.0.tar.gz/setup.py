# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openvpn_ldap_auth']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0', 'PyYAML>=5.4.1,<6.0.0', 'python-ldap>=3.3.1,<4.0.0']

entry_points = \
{'console_scripts': ['openvpn-ldap-auth = openvpn_ldap_auth.main:main']}

setup_kwargs = {
    'name': 'openvpn-ldap-auth',
    'version': '0.1.0',
    'description': 'An auth verify script for OpenVPN to authenticate via LDAP.',
    'long_description': None,
    'author': 'Philipp Hossner',
    'author_email': 'philipph@posteo.de',
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
