# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['get_pwbrowser']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.6.3,<2.0.0',
 'playwright>=1.9.2,<2.0.0',
 'pydantic[dotenv]>=1.8.1,<2.0.0',
 'pyquery>=1.4.3,<2.0.0',
 'tbump>=6.3.1,<7.0.0']

setup_kwargs = {
    'name': 'get-pwbrowser',
    'version': '0.1.1',
    'description': 'instantiate a playwright chromium browser',
    'long_description': None,
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
