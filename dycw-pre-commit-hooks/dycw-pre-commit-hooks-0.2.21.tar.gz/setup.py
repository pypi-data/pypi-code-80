# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dycw_pre_commit_hooks']

package_data = \
{'': ['*']}

install_requires = \
['frozendict>=1.2,<2.0',
 'gitpython>=3.1,<4.0',
 'loguru>=0.5,<0.6',
 'more-itertools>=8.7,<9.0',
 'pyyaml>=5.4,<6.0',
 'toml>=0.10,<0.11']

entry_points = \
{'console_scripts': ['check-settings = '
                     'dycw_pre_commit_hooks.check_settings:main']}

setup_kwargs = {
    'name': 'dycw-pre-commit-hooks',
    'version': '0.2.21',
    'description': 'My pre-commit hooks',
    'long_description': None,
    'author': 'Derek Wan',
    'author_email': 'd.wan@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
