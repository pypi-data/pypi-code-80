# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['john_toolbox']

package_data = \
{'': ['*']}

install_requires = \
['autopep8>=1.5,<2.0',
 'beautifulsoup4>=4.9,<5.0',
 'boto3>=1.16,<2.0',
 'jupyter==1.0.0',
 'jupyter_contrib_nbextensions==0.5.1',
 'jupyterlab==2.1.5',
 'jupytext==1.5.0',
 'matplotlib>=3.1.1,<4.0.0',
 'numpy>=1.19,<2.0',
 'pandas>=1.1,<2.0',
 'sklearn>=0.0.0,<0.0.1',
 'torch>=1.7,<2.0',
 'torchvision>=0.8.1,<0.9.0',
 'tqdm>=4.51,<5.0',
 'xgboost>=1.3,<2.0']

setup_kwargs = {
    'name': 'john-toolbox',
    'version': '0.3.0',
    'description': 'Wrapper for transformers scikit learn pipeline and wrapper for ml model',
    'long_description': '# john-toolbox\n\n\n## how to publish new version in pypi with poetry  ?\nhttps://johnfraney.ca/posts/2019/05/28/create-publish-python-package-poetry/\n\n## how to create a new release\nhttps://www.atlassian.com/fr/git/tutorials/comparing-workflows/gitflow-workflow\n',
    'author': 'john',
    'author_email': 'contact@nguyenjohnathan.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nguyenanht/john-toolbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
