# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esparto']

package_data = \
{'': ['*'], 'esparto': ['templates/*']}

install_requires = \
['Pillow>=7.0.0', 'jinja2>=2.10.1', 'markdown>=3.1']

extras_require = \
{'extras': ['beautifulsoup4>=4.9.3', 'prettierfier>=1.0.3']}

setup_kwargs = {
    'name': 'esparto',
    'version': '0.1.0.dev2',
    'description': 'Simple toolkit for building minimal Bootstrap pages.',
    'long_description': None,
    'author': 'Dominic Thorn',
    'author_email': 'dominic.thorn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
