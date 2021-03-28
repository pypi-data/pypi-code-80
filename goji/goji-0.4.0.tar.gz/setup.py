# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goji']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'requests-html>=0.10.0,<0.11.0',
 'requests[socks]>=2.25.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['goji = goji.commands:cli']}

setup_kwargs = {
    'name': 'goji',
    'version': '0.4.0',
    'description': 'Command line JIRA client',
    'long_description': None,
    'author': 'Kyle Fuller',
    'author_email': 'kyle@fuller.li',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
