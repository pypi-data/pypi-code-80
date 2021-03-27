# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['olxbrasil', 'olxbrasil.parsers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'fake-useragent>=0.1.11,<0.2.0',
 'httpx>=0.17.0,<0.18.0']

setup_kwargs = {
    'name': 'olxbrasil',
    'version': '0.1.0',
    'description': 'Biblioteca para scrapping da Olx Brasil (olx.com.br)',
    'long_description': None,
    'author': 'Marcelo Lino',
    'author_email': 'mdslino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
