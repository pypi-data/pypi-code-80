# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pusnowlib', 'pusnowlib.dj_bus', 'pusnowlib.kaist_bus', 'pusnowlib.kaist_food']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'beautifulsoup4>=4.9.3,<5.0.0']

setup_kwargs = {
    'name': 'pusnowlib',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Wonsup Yoon',
    'author_email': 'pusnow@kaist.ac.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
