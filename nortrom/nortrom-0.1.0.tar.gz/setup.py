# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nortrom']

package_data = \
{'': ['*']}

install_requires = \
['discord-py-slash-command>=1.1.0,<2.0.0', 'discord.py>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'nortrom',
    'version': '0.1.0',
    'description': 'A Discord bot to mute/deafen people',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
