# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teslajsonpy', 'teslajsonpy.homeassistant']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'authcaptureproxy>=0.7.1,<0.8.0',
 'backoff>=1.10.0,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'teslajsonpy',
    'version': '0.17.0',
    'description': 'A library to work with Tesla API.',
    'long_description': None,
    'author': 'Sergey Isachenko',
    'author_email': 'sergey.isachenkol@bool.by',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zabuldon/teslajsonpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
