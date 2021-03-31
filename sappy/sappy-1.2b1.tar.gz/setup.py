# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sappy', 'sappy.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'minilog>=2.0,<3.0']

entry_points = \
{'console_scripts': ['sappy = sappy.cli:main']}

setup_kwargs = {
    'name': 'sappy',
    'version': '1.2b1',
    'description': 'Single-page application server for end-to-end testing.',
    'long_description': '[![Unix Build Status](https://img.shields.io/github/workflow/status/jacebrowning/sappy/main?label=unix)](https://github.com/jacebrowning/sappy/actions?query=branch%3Amain)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/sappy/main.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/sappy)\n[![Coverage Status](http://img.shields.io/coveralls/jacebrowning/sappy/main.svg)](https://coveralls.io/r/jacebrowning/sappy)\n[![Scrutinizer Code Quality](http://img.shields.io/scrutinizer/g/jacebrowning/sappy.svg)](https://scrutinizer-ci.com/g/jacebrowning/sappy/?branch=main)\n[![PyPI Version](http://img.shields.io/pypi/v/sappy.svg)](https://pypi.python.org/pypi/sappy)\n\n# Overview\n\nSappy is a simple, single-page application (SPA) web server for end-to-end testing.\n\nThe Python standard library includes a web server that works great for serving up files:\n\n```sh\n$ python3 -m http.server 8080\nServing HTTP on 0.0.0.0 port 8080 ...\n\n$ curl http://localhost:8080/index.html\n<!DOCTYPE html>\n<html>\n  <head>\n    <title>Example Index</title>\n...\n```\n\nBut when used to serve up single-page applications, a `404` is returned whenever any page other than the index is accessed directly:\n\n```sh\n$ curl http://localhost:8080/login\n<!DOCTYPE html>\n<html lang=en>\n  <title>Error 404 (Not Found)</title\n...\n```\n\nThis project builds on the existing web server code to forward all requests to the index. The single-page application’s client-side routing can then display the page that corresponds to that request’s URL.\n\n# Setup\n\n## Requirements\n\n* Python 3.6+\n\n## Installation\n\nInstall `sappy` with pip:\n\n```sh\n$ pip install sappy\n```\n\nor directly from the source code:\n\n```sh\n$ git clone https://github.com/jacebrowning/sappy.git\n$ cd sappy\n$ python setup.py install\n```\n\n# Usage\n\nBuild your static website (e.g. an Ember application) for production:\n\n```sh\n$ ember build --environment=production\nBuilding...\nBuilt project successfully. Stored in "dist/".\n```\n\nThen serve up the application:\n\n```sh\n$ sappy\nServing /home/browning/project/dist/ on 8080\n```\n\nCheck out the [documentation](http://sappy.readthedocs.io/en/latest/cli) or command-line help for additional options:\n\n```sh\n$ sappy --help\n```\n',
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/sappy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
