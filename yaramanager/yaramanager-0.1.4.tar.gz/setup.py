# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaramanager', 'yaramanager.commands', 'yaramanager.db', 'yaramanager.models']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.2,<2.0.0',
 'alembic>=1.5.8,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'plyara>=2.1.1,<3.0.0',
 'requests>=2.25.1,<3.0.0',
 'rich>=10.0.0,<11.0.0',
 'toml>=0.10.2,<0.11.0',
 'yarabuilder>=0.0.5,<0.0.6']

entry_points = \
{'console_scripts': ['yaramanager = yaramanager.commands.cli:cli',
                     'ym = yaramanager.commands.cli:cli']}

setup_kwargs = {
    'name': 'yaramanager',
    'version': '0.1.4',
    'description': 'CLI tool to manage your yara rules',
    'long_description': '# Yara Manager\nA simple program to manage your yara ruleset in a (sqlite) database.\n\n## Todos\n- [x] Add rules\n- [x] Delete rules\n- [x] List rules\n- [x] Search strings\n- [x] Actually edit rules with `edit` command - currently only file changes are detected, but changes are not merged into the rule itself.\n- [x] Implement rule export\n- [ ] Search rules\n- [ ] Cluster rules in rulesets\n- [ ] Enforce configurable default set of meta fields\n- [ ] Implement backup and sharing possibilities\n- [ ] Add database migrations\n\n## Installation\n```shell\npip install yaramanager\n```\n\n## Features\n### Asciinema\n[![Watch how to use yaramanager](https://asciinema.org/a/HJJoaGaZIdWIFPG8h5AE5kUer.svg)](https://asciinema.org/a/HJJoaGaZIdWIFPG8h5AE5kUer)\nStore your Yara rules in a DB locally and manage them.\n\n### Usage\n```\n$ ym\nUsage: ym [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  add      Add a new rule to the database.\n  config   Review and change yaramanager configuration.\n  db       Manage your databases\n  del      Delete a rule by its ID or name.\n  edit     Edits a rule with your default editor.\n  export   Export rules from the database.\n  get      Get rules from the database.\n  list     Lists rules available in DB.\n  parse    Parses rule files.\n  read     Read rules from stdin.\n  search   Searches through your rules.\n  stats    Prints stats about the database contents.\n  version  Displays the current version.    \n```\n',
    'author': '3c7',
    'author_email': '3c7@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/3c7/yaramanager',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
