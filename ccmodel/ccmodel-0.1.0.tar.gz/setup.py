# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccmodel',
 'ccmodel.__config__',
 'ccmodel.code_models',
 'ccmodel.parsers',
 'ccmodel.rules',
 'ccmodel.utils']

package_data = \
{'': ['*']}

install_requires = \
['clang>=11.0,<12.0', 'graphlib-backport>=1.0.3,<2.0.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'ccmodel',
    'version': '0.1.0',
    'description': 'Python libclang-powered C/C++ code modeling',
    'long_description': '# ccmodel\nPython libclang-powered C/C++ code modeling\n\nVery immature development, not in a useful\nstate yet. No docs.\n',
    'author': 'Gabe Ingram',
    'author_email': 'gabriel.ingram@colorado.edu',
    'maintainer': 'Gabe Ingram',
    'maintainer_email': 'gabriel.ingram@colorado.edu',
    'url': 'https://github.com/gjingram/ccmodel',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
