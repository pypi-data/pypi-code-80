# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_socio_grpc',
 'django_socio_grpc.management',
 'django_socio_grpc.management.commands',
 'django_socio_grpc.protobuf',
 'django_socio_grpc.utils']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0',
 'djangorestframework>=3.10.0,<4.0.0',
 'grpcio-tools>=1.16.0,<2.0.0',
 'grpcio>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'django-socio-grpc',
    'version': '0.1.0',
    'description': 'Fork of django-grpc-framework with more feature maintained by the socio team. Make GRPC with django easy.',
    'long_description': None,
    'author': 'Adrien Montagu',
    'author_email': 'adrienmontagu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
