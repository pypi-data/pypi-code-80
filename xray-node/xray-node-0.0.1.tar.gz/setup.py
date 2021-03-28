# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xray_node', 'xray_node.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'httpx>=0.17.1,<0.18.0']

entry_points = \
{'console_scripts': ['xnode = xray_node.main:main']}

setup_kwargs = {
    'name': 'xray-node',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'laoshan-taoist',
    'author_email': '65347330+laoshan-taoist@users.noreply.github.com',
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
