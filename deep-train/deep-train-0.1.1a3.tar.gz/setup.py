# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deep_train',
 'deep_train.common',
 'deep_train.pytorch',
 'deep_train.pytorch.tasks']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.20.1,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'tensorboard>=2.4.1,<3.0.0',
 'torch>=1.8.0,<2.0.0',
 'tqdm>=4.59.0,<5.0.0']

setup_kwargs = {
    'name': 'deep-train',
    'version': '0.1.1a3',
    'description': 'Decoupled training for PyTorch',
    'long_description': '',
    'author': 'Harsh Saini',
    'author_email': 'harshsaini90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/harshsaini/deep-train',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
