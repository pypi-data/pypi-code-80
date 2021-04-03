# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kindlenotes2md']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyquery>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['kindlenotes2md = kindlenotes2md.notes:cli']}

setup_kwargs = {
    'name': 'kindlenotes2md',
    'version': '0.1.2',
    'description': 'Convert your kindle notes to markdown format',
    'long_description': "# kindlenotes2md\n\nCommand line utility to convert your Kindle highlights from html to markdown.\n\n\n## Installation\n\n```\npip install kindlenotes2md\n```\n\n## Usage\n\nFrom the Kindle app, you have the option to export the highlights that you've made in the book.\nThe easiest way to get access to these are to email them to yourself.\nThese exported highlights are in html format, so are a bit tricky to use in other tools.\n\nRun this tool with the `.html` file as a command line argument.\n\n```\nkindlenotes2md INPUTFILENAME\n```\n\nHere's the documentation for the tool you get by running `--help`.\n\n```\nUsage: kindlenotes2md [OPTIONS] INPUTFILENAME\n\nOptions:\n  -o, --outfilename TEXT\n  --help                  Show this message and exit.\n```\n\nYou have the option to specify a filename with `-o` or `--outfilename`.\nThis will write the markdown output to file, rather than stdout.\n",
    'author': 'Ewan Nicolson',
    'author_email': 'ewan.nicolson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dataewan/kindlenotes2md',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
