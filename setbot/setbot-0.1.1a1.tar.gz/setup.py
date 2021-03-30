# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['setbot']
install_requires = \
['aiohttp>=3.7.4,<4.0.0', 'pytz>=2021.1,<2022.0', 'slack-sdk>=3.4.2,<4.0.0']

entry_points = \
{'console_scripts': ['setbot = setbot:main']}

setup_kwargs = {
    'name': 'setbot',
    'version': '0.1.1a1',
    'description': 'I respond to daily set scores with emoji',
    'long_description': None,
    'author': 'Vasundhara',
    'author_email': 'vasundhara131719@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
