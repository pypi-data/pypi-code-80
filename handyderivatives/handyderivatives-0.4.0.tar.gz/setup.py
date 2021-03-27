# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['handyderivatives']

package_data = \
{'': ['*']}

install_requires = \
['sympy>=1.7.1,<2.0.0']

entry_points = \
{'console_scripts': ['handyderivatives = handyderivatives:main']}

setup_kwargs = {
    'name': 'handyderivatives',
    'version': '0.4.0',
    'description': 'A simple little to batch process some basic calc stuff.',
    'long_description': '# handyderivatives\n\n## Running it\n`python handyderivatives.py functions.txt`\n\n## How to use it\nIt gets the derivatives for differentiable functions of a single variable.\n\nEdit a config file that looks like this. \n\n![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/file.png)\n\nTo get output that looks like this. LaTex output is included.\n\n![Placeholder](https://raw.githubusercontent.com/Fitzy1293/handyderivatives/main/output.png)\n',
    'author': 'fitzy1293',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
