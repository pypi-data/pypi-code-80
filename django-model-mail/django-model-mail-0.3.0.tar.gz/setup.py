# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['model_mail']

package_data = \
{'': ['*'], 'model_mail': ['templates/model_mail/*']}

install_requires = \
['Django>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'django-model-mail',
    'version': '0.3.0',
    'description': "Django package that helps to create emails from models (e.g. for admins' notifications)",
    'long_description': "=================\nDjango Model Mail\n=================\n\n\n.. image:: https://img.shields.io/pypi/v/django-model-mail.svg\n        :target: https://pypi.python.org/pypi/django-model-mail\n\n.. image:: https://img.shields.io/travis/la1t/django-model-mail.svg\n        :target: https://travis-ci.org/la1t/django-model-mail\n\n\nDjango package that helps to create emails from models (e.g. for admins' notifications)\n\n\n* Free software: MIT license\n\n\nFeatures\n--------\n\n* TODO\n\n\nDeploying\n---------\n\nA reminder for the maintainers on how to deploy.\nMake sure all your changes are committed (including an entry in HISTORY.rst).\nThen run::\n\n$ poetry version patch # possible: major / minor / patch\n$ git push\n$ git push --tags\n\nTravis will then deploy to PyPI if tests pass.\n",
    'author': 'Anatoly Gusev',
    'author_email': 'gusev.tolia@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/la1t/django-model-mail',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
