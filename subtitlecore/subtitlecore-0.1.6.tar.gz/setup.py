# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subtitlecore']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'pip>=21.0.1,<22.0.0',
 'spacy>=3.0.5,<4.0.0',
 'webvtt-py>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['subtitlecore_content = '
                     'subtitlecore.entry:get_subtitle_content',
                     'subtitlecore_parse2sens = subtitlecore.entry:parse2sens',
                     'subtitlecore_parse2text = subtitlecore.entry:parse2text']}

setup_kwargs = {
    'name': 'subtitlecore',
    'version': '0.1.6',
    'description': 'Parse srt file content into well-formed structures',
    'long_description': None,
    'author': 'Phoenix.Grey',
    'author_email': 'phoenix.grey0108@gmail.com',
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
