# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mutagen_helper', 'mutagen_helper.test']

package_data = \
{'': ['*'], 'mutagen_helper.test': ['data/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click>=7.1.2,<8.0.0', 'expandvars>=0.6.5,<0.7.0']

entry_points = \
{'console_scripts': ['mutagen-helper = mutagen_helper.__main__:main']}

setup_kwargs = {
    'name': 'mutagen-helper',
    'version': '1.2.0',
    'description': 'Mutagen Helper allow you to define Mutagen synchronisation sessions inside a configuration file on directories you want to synchronise. Created sessions are marked with a session name and a project name that makes them easier to manage.',
    'long_description': None,
    'author': 'Rémi Alvergnat',
    'author_email': 'toilal.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gfi-centre-ouest/mutagen-helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
