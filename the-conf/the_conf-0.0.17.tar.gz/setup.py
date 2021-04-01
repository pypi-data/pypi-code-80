# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['the_conf']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3,<6.0']

setup_kwargs = {
    'name': 'the-conf',
    'version': '0.0.17',
    'description': 'Config build from multiple sources',
    'long_description': None,
    'author': 'François Schmidts',
    'author_email': 'francois@schmidts.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
