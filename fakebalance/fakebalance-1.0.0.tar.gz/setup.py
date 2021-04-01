# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['fakebalance']
setup_kwargs = {
    'name': 'fakebalance',
    'version': '1.0.0',
    'description': 'fakebalance qiwi\\sber',
    'long_description': None,
    'author': 'Ilya Romanov',
    'author_email': 'rolton-tv@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
