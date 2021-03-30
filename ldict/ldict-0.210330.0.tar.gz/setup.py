# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['ldict']
install_requires = \
['garoupa>=1.210328.3,<2.0.0', 'orjson>=3.5.0,<4.0.0', 'pylint>=2.7.4,<3.0.0']

setup_kwargs = {
    'name': 'ldict',
    'version': '0.210330.0',
    'description': 'Uniquely identified lazy dict',
    'long_description': None,
    'author': 'davips',
    'author_email': 'dpsabc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
