# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sister']

package_data = \
{'': ['*']}

install_requires = \
['Janome==0.3.10',
 'fasttext==0.9.2',
 'gensim==3.8.3',
 'mecab-python3==0.996.5',
 'numpy==1.19.0',
 'progressbar>=2.5,<3.0',
 'torch==1.5.1',
 'transformers==2.11.0']

setup_kwargs = {
    'name': 'sister',
    'version': '0.2.1',
    'description': 'SISTER (SImple SenTence EmbeddeR)',
    'long_description': None,
    'author': 'sobamchan',
    'author_email': 'oh.sore.sore.soutarou@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
