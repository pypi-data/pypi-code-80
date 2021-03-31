# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfactory',
 'cfactory.__config__',
 'cfactory.collections',
 'cfactory.std_factories',
 'cfactory.std_factories.bindings',
 'cfactory.std_factories.bindings.pybind',
 'cfactory.utils']

package_data = \
{'': ['*'], 'cfactory.std_factories': ['templates/*', 'templates/pybind/*']}

install_requires = \
['ccmodel>=0.1.0,<0.2.0',
 'graphlib-backport>=1.0.3,<2.0.0',
 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'cfactory',
    'version': '0.1.0',
    'description': 'C/C++, et al., metaprogramming tool implemented in python',
    'long_description': '# cfactory\nC/C++, et al., metaprogramming tool implemented in python\n',
    'author': 'Gabe Ingram',
    'author_email': 'gabriel.ingram@colorado.edu',
    'maintainer': 'Gabe Ingram',
    'maintainer_email': 'gabriel.ingram@colorado.edu',
    'url': 'https://github.com/gjingram/cfactory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
