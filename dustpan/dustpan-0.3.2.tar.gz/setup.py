# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dustpan']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0', 'colorama>=0.4.4,<0.5.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['dustpan = dustpan.__main__:main']}

setup_kwargs = {
    'name': 'dustpan',
    'version': '0.3.2',
    'description': '',
    'long_description': '# `dustpan`\n\n[![pypi version](https://img.shields.io/pypi/v/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)\n[![downloads](https://pepy.tech/badge/dustpan)](https://pepy.tech/project/dustpan)\n[![build status](https://github.com/dawsonbooth/dustpan/workflows/build/badge.svg)](https://github.com/dawsonbooth/dustpan/actions?workflow=build)\n[![python versions](https://img.shields.io/pypi/pyversions/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)\n[![format](https://img.shields.io/pypi/format/dustpan.svg?style=flat)](https://pypi.org/pypi/dustpan/)\n[![license](https://img.shields.io/pypi/l/dustpan.svg?style=flat)](https://github.com/dawsonbooth/dustpan/blob/master/LICENSE)\n\n## Description\n\nClean up your workspace by removing extraneous files and directories.\n\n## Installation\n\nWith [Python](https://www.python.org/downloads/) installed, simply run the following command to add the package to your project.\n\n```bash\npython -m pip install dustpan\n```\n\n## Usage\n\nThis is a command-line program, and can be executed as follows:\n\n```bash\ndustpan [-h] [-p PATTERNS [PATTERNS ...]] [-i IGNORE [IGNORE ...]] [--remove-empty-directories] [-q | -v | -vv] directories [directories ...]\n```\n\nPositional arguments:\n\n```txt\n  directories           Root directories to search\n```\n\nOptional arguments:\n\n```txt\n  -h, --help            show this help message and exit\n  -p PATTERNS [PATTERNS ...], --patterns PATTERNS [PATTERNS ...]\n                        Additional path patterns to queue for removal\n  -i IGNORE [IGNORE ...], --ignore IGNORE [IGNORE ...]\n                        Path patterns to exclude from removal\n  --remove-empty-directories\n                        Remove all childless directories\n  -q, --quiet           Be quiet\n  -v, --verbose         Be more verbose\n  -vv, --very-verbose   Be very verbose\n```\n\nFeel free to [check out the docs](https://dawsonbooth.github.io/dustpan/) for more information on how to use this package.\n\n## License\n\nThis software is released under the terms of [MIT license](LICENSE).\n',
    'author': 'Dawson Booth',
    'author_email': 'pypi@dawsonbooth.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dawsonbooth/dustpan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
