# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rundeckpy']

package_data = \
{'': ['*']}

install_requires = \
['paramiko>=2.7.2,<3.0.0']

setup_kwargs = {
    'name': 'rundeckpy',
    'version': '0.1.10',
    'description': '',
    'long_description': None,
    'author': 'Thiago Takayama',
    'author_email': 'thiago@takayama.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
