# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat', 'mdformat.codepoints', 'mdformat.renderer']

package_data = \
{'': ['*']}

install_requires = \
['markdown-it-py>=0.5.5,<0.7.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=0.12',
                             'typing-extensions>=3.7.4']}

entry_points = \
{'console_scripts': ['mdformat = mdformat.__main__:run']}

setup_kwargs = {
    'name': 'mdformat',
    'version': '0.6.3',
    'description': 'CommonMark compliant Markdown formatter',
    'long_description': "[![Documentation Status](https://readthedocs.org/projects/mdformat/badge/?version=latest)](https://mdformat.readthedocs.io/en/latest/?badge=latest)\n[![Build Status](https://github.com/executablebooks/mdformat/workflows/Tests/badge.svg?branch=master)](https://github.com/executablebooks/mdformat/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)\n[![codecov.io](https://codecov.io/gh/executablebooks/mdformat/branch/master/graph/badge.svg)](https://codecov.io/gh/executablebooks/mdformat)\n[![PyPI version](https://img.shields.io/pypi/v/mdformat)](https://pypi.org/project/mdformat)\n\n# ![mdformat](https://raw.githubusercontent.com/executablebooks/mdformat/master/docs/_static/logo.svg)\n\n> CommonMark compliant Markdown formatter\n\n<!-- start mini-description -->\n\nMdformat is an opinionated Markdown formatter\nthat can be used to enforce a consistent style in Markdown files.\nMdformat is a Unix-style command-line tool as well as a Python library.\n\n<!-- end mini-description -->\n\nFind out more in the [docs](https://mdformat.readthedocs.io).\n\n<!-- start installing -->\n\n## Installing\n\nInstall with CommonMark support:\n\n```bash\npip install mdformat\n```\n\nAlternatively install with GitHub Flavored Markdown (GFM) support:\n\n```bash\npip install mdformat-gfm\n```\n\n<!-- end installing -->\n\n<!-- start cli-usage -->\n\n## Command line usage\n\n### Format files\n\nFormat files `README.md` and `CHANGELOG.md` in place\n\n```bash\nmdformat README.md CHANGELOG.md\n```\n\nFormat `.md` files in current working directory recursively\n\n```bash\nmdformat .\n```\n\nRead Markdown from standard input until `EOF`.\nWrite formatted Markdown to standard output.\n\n```bash\nmdformat -\n```\n\n### Check formatting\n\n```bash\nmdformat --check README.md CHANGELOG.md\n```\n\nThis will not apply any changes to the files.\nIf a file is not properly formatted, the exit code will be non-zero.\n\n### Options\n\n```console\nfoo@bar:~$ mdformat --help\nusage: mdformat [-h] [--check] [--version] [--number]\n                [--wrap {keep,no,INTEGER}]\n                [paths [paths ...]]\n\nCommonMark compliant Markdown formatter\n\npositional arguments:\n  paths                 files to format\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --check               do not apply changes to files\n  --version             show program's version number and exit\n  --number              apply consecutive numbering to ordered lists\n  --wrap {keep,no,INTEGER}\n                        paragraph word wrap mode (default: keep)\n```\n\n<!-- end cli-usage -->\n\n## Documentation\n\nThis README merely provides a quickstart guide for the command line interface.\nFor more information refer to the [documentation](https://mdformat.readthedocs.io).\nHere's a few pointers to get you started:\n\n- [Style guide](https://mdformat.readthedocs.io/en/stable/users/style.html)\n- [Python API usage](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html#python-api-usage)\n- [Usage as a pre-commit hook](https://mdformat.readthedocs.io/en/stable/users/installation_and_usage.html#usage-as-a-pre-commit-hook)\n- Plugins\n  - [Plugin usage](https://mdformat.readthedocs.io/en/stable/users/plugins.html)\n  - [Plugin development guide](https://mdformat.readthedocs.io/en/stable/developers/contributing.html)\n  - [List of existing plugins](https://mdformat.readthedocs.io/en/stable/users/plugins.html)\n- [Changelog](https://mdformat.readthedocs.io/en/stable/users/changelog.html)\n\n## Frequently Asked Questions\n\n### What's wrong with the mdformat logo? It renders incorrectly and is just terrible in general.\n\nNope, the logo is actually pretty great – you're terrible.\nThe logo is more a piece of art than a logo anyways,\ndepicting the horrors of poorly formatted text documents.\nI made it myself.\n",
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/executablebooks/mdformat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
