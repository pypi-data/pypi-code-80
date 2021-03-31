# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['x2cdict', 'x2cdict.db']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'googletrans==4.0.0-rc1', 'pymongo>=3.10.1,<4.0.0']

entry_points = \
{'console_scripts': ['x2cdict_phrase = x2cdict.entry:search_phrase',
                     'x2cdict_vocab = x2cdict.entry:search_vocab',
                     'x2cdict_vocab_without_pos = '
                     'x2cdict.entry:search_vocab_without_pos']}

setup_kwargs = {
    'name': 'x2cdict',
    'version': '0.1.39',
    'description': 'translate X language into Chinese',
    'long_description': None,
    'author': 'Phoenix Grey',
    'author_email': 'phoenix.grey0108@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
