# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scholar_network']

package_data = \
{'': ['*']}

install_requires = \
['dash-bootstrap-components>=0.12.0,<0.13.0',
 'dash>=1.19.0,<2.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'networkx>=2.5,<3.0',
 'pandas>=1.2.3,<2.0.0',
 'plotly>=4.14.3,<5.0.0',
 'scipy>=1.6.2,<2.0.0',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'scholar-network',
    'version': '0.1.0',
    'description': 'Network Analysis and Web App for IPOP scholars',
    'long_description': '# stuff\n',
    'author': 'Nick Anthony',
    'author_email': 'nanthony007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
