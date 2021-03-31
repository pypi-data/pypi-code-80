# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['remarkdav']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=1.26.0,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'dateparser>=1.0.0,<2.0.0',
 'dynaconf>=3.1.2,<4.0.0',
 'fpdf>=1.7.2,<2.0.0',
 'peewee>=3.14.0,<4.0.0',
 'rmapy>=0.2.2,<0.3.0',
 'webdavclient3>=3.14.5,<4.0.0']

entry_points = \
{'console_scripts': ['remarkdav = remarkdav.cli:cli']}

setup_kwargs = {
    'name': 'remarkdav',
    'version': '1.0.post0',
    'description': 'A tool to sync webdav files (only PDF) to the reMarkable cloud',
    'long_description': 'remarkdav\n=========\nThis is a small tool to sync webdav files (only PDF) to the reMarkable cloud (oneway).\n\nSetup (dev)\n-----------\n\n1. Get rmapi (Go CLI application)\n\nsee instructions at https://github.com/juruen/rmapi\n\n2. Clone from Git\n\n.. code-block::\n\n    git clone git@github.com:hansegucker/remarkdav.git\n\n3. Get poetry\n\nSee instructions at https://python-poetry.org/docs/#installation\n\n\n4. Install dependencies\n\n.. code-block::\n\n    $ cd remarkdav/ # Go to your cloned directory\n    $ poetry install\n\n5. Run\n\n.. code-block::\n\n    $ poetry run remarkdav\n\nSetup (production)\n------------------\n\n1. Get rmapi (Go CLI application)\n\nsee instructions at https://github.com/juruen/rmapi\n\n2. Get it via poetry (use pip with Python 3)\n\n.. code-block::\n\n    $ sudo pip install -G remarkdav\n\n3. Run\n\n.. code-block::\n\n    $ remarkdav\n\nConfiguration\n-------------\nCopy the example configuration file from ``settings-example.toml`` to ``/etc/remarkdav/settings.toml`` and customise it.\n\n\nCopyright\n---------\n© 2020 by Jonathan Weth <dev@jonathanweth.de>\n\nremarkdav is licenced under GPL-3.0.',
    'author': 'Jonathan Weth',
    'author_email': 'dev@jonathanweth.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
