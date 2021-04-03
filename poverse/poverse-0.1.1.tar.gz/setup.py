# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poverse']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['poverse = poverse.cli:cli']}

setup_kwargs = {
    'name': 'poverse',
    'version': '0.1.1',
    'description': 'Get the installed version of dependency within poetry.lock file',
    'long_description': '# poverse: Gets the version of dependencies installed by Poetry\n\n[Poetry](https://python-poetry.org/) is a great tool for managing python projects. This small library retrieves the version of an installed package.\n\nSupports python versions >=3.7, <=3.9\n\n## Installation\n\n```sh\n$ pip install poverse\n```\n\n## Usage\n\n### Cli\n\n```bash\n$ poverse --help\nUsage: poverse [OPTIONS] [LOCK_FILE_PATH]\n\n  Looks for package with name in LOCK_FILE_PATH.\n\n  LOCK_FILE_PATH is the path to Poetry lock file defaults to\n  `$PWD/poetry.lock` if not supplied\n\nOptions:\n  -p, --package TEXT  Name of the package in lock file  [required]\n  --help              Show this message and exit.\n```\n\n#### Example usage\n\n```sh\n$ poverse -p click\n7.1.2\n\n$ poverse -p click $PWD/tests/test_data/poetry.lock\n7.1.2\n```\n\n### API\n\n**`get_installed_version`**\n\nGets the actual installed version for the supplied package with name\nfrom the poetry lock.\n\n**Params:**\n- `package_name` (_**required**, str_): name of the package that could be in the lock file (required)\n- `lock_file_path` (_str_): path to `poetry.lock` file. Defaults to a `poetry.lock` in the current directory.\n\n**Returns:** _Optional[str]_ - Version of requested dependency, `None` if package does not exist.\n\n#### Examples\n\n```python\nfrom poverse import get_installed_version\n\nget_installed_version("boto3") # Get the installed version of boto3 from project\'s poetry.lock\n\nget_installed_version("boto3", "/home/user/projects/project/poetry.lock") # Get the installed version of boto3 from the poetry lock supplied\n```\n\n## Motivation\n\nThe idea behind this project is for applications where you perhaps need to install specific versions of binaries (e.g. Spark or GDAL) that are dependent on your application dependencies.\n\n## Development\n\nFound something that should not be happening? Do you have an idea that would make this library great? Raise an issue or PR, contributions welcome!\n',
    'author': 'Joel Clemence',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JoelClemence/poverse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
