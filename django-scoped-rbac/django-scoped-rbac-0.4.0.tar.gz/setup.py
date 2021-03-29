# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'cel-python/src'}

packages = \
['celpy', 'scoped_rbac', 'scoped_rbac.migrations', 'xlate']

package_data = \
{'': ['*']}

install_requires = \
['Babel>=2.9.0,<3.0.0',
 'django-jsonfield-backport>=1.0.3,<2.0.0',
 'django-rest-framework-condition>=0.1.0,<0.2.0',
 'django>=2.2.8,<3.0.0',
 'djangorestframework>=3.11.0,<4.0.0',
 'drf-extensions>=0.6.0,<0.7.0',
 'jmespath>=0.10.0,<0.11.0',
 'lark-parser>=0.8.5,<0.9.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.25.0,<3.0.0',
 'scrudful>=0.1.0,<0.2.0',
 'urllib3>=1.26.1,<2.0.0']

setup_kwargs = {
    'name': 'django-scoped-rbac',
    'version': '0.4.0',
    'description': 'A rich and flexible Django application for role-based access control within distinct access control scopes supporting Django Rest Framework.',
    'long_description': None,
    'author': 'David Charboneau',
    'author_email': 'david@adadabase.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/openteams/django-scoped-rbac',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.6,<4.0.0',
}


setup(**setup_kwargs)
