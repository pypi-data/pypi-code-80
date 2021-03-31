# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getgist']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.6', 'requests>=2.18.1', 'tabulate>=0.8.7']

entry_points = \
{'console_scripts': ['getgist = getgist.__main__:run_getgist',
                     'getmy = getgist.__main__:run_getmy',
                     'lsgists = getgist.__main__:run_lsgists',
                     'putgist = getgist.__main__:run_putgist',
                     'putmy = getgist.__main__:run_putmy']}

setup_kwargs = {
    'name': 'getgist',
    'version': '0.2.1',
    'description': 'CLI to update local and remote files from GitHub Gists.',
    'long_description': "[![Travis CI](https://img.shields.io/travis/cuducos/getgist.svg?style=flat)](https://travis-ci.org/cuducos/getgist) [![Coveralls](https://img.shields.io/coveralls/cuducos/getgist.svg?style=flat)](https://coveralls.io/github/cuducos/getgist) [![PyPI Version](https://img.shields.io/pypi/v/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist) [![Python Version](https://img.shields.io/pypi/pyversions/getgist.svg?style=flat)](https://pypi.python.org/pypi/getgist)\n\n# GetGist\n\nEasily download any file from a [GitHub Gist](http://gist.github.com), with _one single command_.\n\n## Why?\n\nBecause of reasons I do not have a *dotfiles* repository. I prefer to store my `init.vim`, `.gitconfig`, `.bashrc` etc. as [Gists](http://gist.github.com/).\n\nI wrote this CLI so I could update my *dotfiles* with one single command: `getmy vim.init`, for example — and it's done.\n\n## Install\n\n```console\n$ pip install getgist\n```\n\n_GetGist_ works with Python 3.6+.\n\nTo **update** it just run `$ pip install --upgrade getgist`.\n\n## Usage\n\n### Getting Gists from GitHub\n\nJust run `getgist <username> <filename>`. For example:\n\n```console\n$ getgist cuducos .vimrc\n  Fetching https://api.github.com/users/cuducos/gists\n  Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc\n  Saving .vimrc\n  Done!\n```\n\n_GetGist_ asks you what to do when a local file (with the same name) exists. If you decide not to delete your local copy of the file, it will be renamed with extensions such as `.bkp`, `.bkp1`, `.bkp2` etc.\n\n### Updating Gists at GitHub\n\nJust run `putgist <username> <filename>` to update the remote Gist with the contents of the local file. It requires an OAuth token (see [Using OAuth authentication](#using-oauth-authentication) below). For example:\n\n```console\n$ putgist cuducos .vimrc\n  User cuducos authenticated\n  Fetching https://api.github.com/gists\n  Sending contents of .vimrc to https://api.github.com/gists/409fac6ac23bf515f495\n  Done!\n  The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495\n```\n\n_GetGist_ asks you what to do when it finds the different files with the same name in different Gists.\n\n### Listing Gist files from GitHub\n\nJust run `lsgists <username>`. For example:\n\n```console\n$ lsgists cuducos\n  Gist           File               URL\n  -------------  ------------------ -------------------------\n  First Gist     file.md            https://gist.github.com/…\n  My Gist #2     another_file.md    https://gist.github.com/…\n  My Gist #2     README.md          https://gist.github.com/…\n```\n\nSecret Gists (when user is authenticated) are listed with `[Secret Gist]` tag next to their names.\n\n## Using OAuth authentication\n\n### Why?\n\nAdd your [personal access token](https://github.com/settings/tokens) as as environment variable to allow:\n\n1. downloading private gists\n2. updating existing gists\n3. listing private gists\n\n### How?\n\n1. Get a personal access token with permission to manage your gists from [GitHub settings](https://github.com/settings/tokens)\n2. Set an environment variable called `GETGIST_TOKEN` with your personal access token\n\nThis [article](https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-set-environment-variables-in-linux/) might help you create an environment variable in a Unix-based operational system with Bash, but feel free to search alternatives for other systems and shells.\n\n### Example\n\n```console\n$ export GETGIST_TOKEN=whatever1234\n$ getgist cuducos .vimrc\n  User cuducos authenticated\n  Fetching https://api.github.com/gists\n  Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc\n  Saving .vimrc\n  Done!\n  The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495\n```\n\nThis will work even if the file you are trying to download is a private gist (surely the user name has to match the `GETGIST_TOKEN` account).\n\n## Setting a default user\n\n### Why?\n\nSet a default user to avoid typing your GitHub user name all the time.\n\n### How?\n\n1. Set an environment variable called `GETGIST_USER` with your GitHub user name\n2. Use the shortcut `getmy <filename>`, `putmy <filename>` or `mygists`\n\n### Example\n\n```console\n$ export GETGIST_USER=cuducos\n$ getmy .vimrc\n  Fetching https://api.github.com/users/cuducos/gists\n  Reading https://gist.githubusercontent.com/cuducos/409fac6ac23bf515f495/raw/666d7d01a0058e4fd898ff752db66160f10a60bb/.vimrc\n  Saving .vimrc\n  Done!\n  The URL to this Gist is: https://gist.github.com/cuducos/409fac6ac23bf515f495\n```\n\n## Contributing\n\nWe use [Poetry](https://python-poetry.org) to manage our development environment:\n\n1. `poetry install` will get you a virtualenv with all the dependencies for you\n1. `poetry shell` will activate this virtualenv\n1. `exit` deactivates this virtualenv\n\nFeel free to [report an issue](http://github.com/cuducos/getgist/issues), [open a pull request](http://github.com/cuducos/getgist/pulls), or [drop a line](http://twitter.com/cuducos).\n\nDon't forget to format your code with [Black](https://github.com/ambv/black), and to write and run tests:\n\n```console\n$ tox\n```\n",
    'author': 'Eduardo Cuducos',
    'author_email': 'cuducos@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/cuducos/getgist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
