# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinxcontrib', 'sphinxcontrib.autodoc_pydantic']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.0', 'pydantic>=1.0']

setup_kwargs = {
    'name': 'autodoc-pydantic',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mansenfranzen',
    'author_email': 'franz.woellert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1',
}


setup(**setup_kwargs)
