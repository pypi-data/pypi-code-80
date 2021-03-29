# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_plan',
 'git_plan.cli',
 'git_plan.cli.commands',
 'git_plan.model',
 'git_plan.service',
 'git_plan.util']

package_data = \
{'': ['*']}

install_requires = \
['cachetools>=4.2.1,<5.0.0',
 'dependency-injector[yaml]>=4.31.1,<5.0.0',
 'humanize>=3.3.0,<4.0.0',
 'inquirer>=2.7.0,<3.0.0',
 'rich>=9.13.0,<10.0.0']

entry_points = \
{'console_scripts': ['git-plan = git_plan.__cli__:main',
                     'gp = git_plan.__cli__:main']}

setup_kwargs = {
    'name': 'git-plan',
    'version': '0.2.3',
    'description': 'A better personal workflow for git',
    'long_description': None,
    'author': 'Rory Byrne',
    'author_email': 'rory@rory.bio',
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
