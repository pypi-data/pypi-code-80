# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['iflearn']
setup_kwargs = {
    'name': 'iflearn',
    'version': '1.0.0',
    'description': 'Test if (the lib for book)',
    'long_description': None,
    'author': 'tikotstudio',
    'author_email': 'tikotstudio@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
