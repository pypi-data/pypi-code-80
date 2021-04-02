# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '..'}

packages = \
['nonebot_plugin_nodice']

package_data = \
{'': ['*'], 'nonebot_plugin_nodice': ['dist/*']}

install_requires = \
['hjson>=3.0.2,<4.0.0', 'nonebot-adapter-cqhttp>=2.0.0a11.post2,<3.0.0']

extras_require = \
{'nb1': ['nonebot>=1.8.2,<2.0.0'], 'nb2': ['nonebot2>=2.0.0-alpha.11,<3.0.0']}

setup_kwargs = {
    'name': 'nonebot-plugin-nodice',
    'version': '2.0.0a1',
    'description': 'Dicebot Pulgin for Nonebot',
    'long_description': None,
    'author': 'Jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
