# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_avro']

package_data = \
{'': ['*']}

install_requires = \
['fastavro>=1.3.4,<2.0.0',
 'singer-python>=5,<6',
 'smart_open>=4.2.0,<5.0.0',
 'strict_rfc3339>=0.7,<0.8']

entry_points = \
{'console_scripts': ['fmt = scripts:fmt',
                     'lint = scripts:lint',
                     'target-avro = target_avro:main',
                     'test = scripts:test']}

setup_kwargs = {
    'name': 'target-avro',
    'version': '0.1.1',
    'description': 'Singer.io target for extracting data',
    'long_description': None,
    'author': 'inamura',
    'author_email': 'inamura@kageboushi.app',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
