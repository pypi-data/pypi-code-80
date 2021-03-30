# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['useis',
 'useis.clients',
 'useis.clients.old_api_client',
 'useis.core',
 'useis.processors',
 'useis.settings']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.4,<4.0.0', 'uquake>=0.4.33,<0.5.0']

setup_kwargs = {
    'name': 'useis',
    'version': '0.1.10',
    'description': '',
    'long_description': None,
    'author': 'jpmercier',
    'author_email': 'jpmercier01@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
