# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mitol',
 'mitol.authentication',
 'mitol.authentication.migrations',
 'mitol.authentication.settings',
 'mitol.authentication.urls',
 'mitol.authentication.views']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2.12,<3.0.0',
 'djangorestframework>=3.0.0,<4.0.0',
 'mitol-django-common>=0.6.0,<0.7.0',
 'mitol-django-mail>=0.4.0,<0.5.0',
 'python3-saml>=1.10.1,<2.0.0',
 'social-auth-app-django>=3.1.0,<4.0.0',
 'social-auth-core>=3.3.3,<4.0.0']

setup_kwargs = {
    'name': 'mitol-django-authentication',
    'version': '0.2.0',
    'description': 'MIT Open Learning django app extensions for social-auth',
    'long_description': None,
    'author': 'MIT Office of Open Learning',
    'author_email': 'mitx-devops@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
