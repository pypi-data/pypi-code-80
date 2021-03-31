# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vlttng']

package_data = \
{'': ['*'], 'vlttng': ['profiles/*']}

install_requires = \
['pyyaml>=5.1,<6.0', 'setuptools', 'termcolor>=1.1,<2.0']

entry_points = \
{'console_scripts': ['vlttng = vlttng.vlttng_cli:run',
                     'vlttng-quick = vlttng.vlttng_quick_cli:run']}

setup_kwargs = {
    'name': 'vlttng',
    'version': '0.10.4',
    'description': 'Generator of LTTng virtual environment',
    'long_description': None,
    'author': 'Philippe Proulx',
    'author_email': 'eeppeliteloop@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eepp/vlttng/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
