# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['multicommand']
setup_kwargs = {
    'name': 'multicommand',
    'version': '0.0.4',
    'description': 'Simple subcommand CLIs with argparse',
    'long_description': '# multicommand\n\nSimple subcommand CLIs with argparse.\n\n## Installation\n\n```bash\npip install multicommand\n```\n\n## Overview\n\n`multicommand` enables you to easily write CLIs with deeply nested (sub)commands using argparse. Just created the directory structure that reflects the CLI command structure you want, write your parsers in "isolation" and multi command will do the rest.\n\nmulticommand turns a directory structure like this:\n\n```text\ncommands/unary/negate.py\ncommands/binary/add.py\ncommands/binary/divide.py\ncommands/binary/multiply.py\ncommands/binary/subtract.py\n```\n\nTurns into a command line application like this:\n\n```bash\nmycli unary negate ...\nmycli binary add ...\nmycli binary divide ...\nmycli binary multiply ...\nmycli binary subtract ...\n```\n\n## Getting Started\n\nSee the [simple example](examples/01_simple/README.md).\n',
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewrosss/multicommand',
    'py_modules': modules,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
