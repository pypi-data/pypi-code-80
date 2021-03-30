# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prodapi', 'prodapi.models', 'prodapi.routes']

package_data = \
{'': ['*']}

install_requires = \
['fastapi-security>=0.3.1,<0.4.0', 'orjson>=3,<4']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=3,<4']}

setup_kwargs = {
    'name': 'prodapi',
    'version': '0.1.0',
    'description': 'A thin layer on top of FastAPI that adds some production readiness features.',
    'long_description': '# prodapi\n\n[![Continuous Integration Status](https://github.com/jmagnusson/prodapi/actions/workflows/ci.yml/badge.svg)](https://github.com/jmagnusson/prodapi/actions/workflows/ci.yml)\n[![Continuous Delivery Status](https://github.com/jmagnusson/prodapi/actions/workflows/cd.yml/badge.svg)](https://github.com/jmagnusson/prodapi/actions/workflows/cd.yml)\n[![Python Versions](https://img.shields.io/pypi/pyversions/prodapi.svg)](https://pypi.org/project/prodapi/)\n[![Code Coverage](https://img.shields.io/codecov/c/github/jmagnusson/prodapi?color=%2334D058)](https://codecov.io/gh/jmagnusson/prodapi)\n[![PyPI Package](https://img.shields.io/pypi/v/prodapi?color=%2334D058&label=pypi%20package)](https://pypi.org/project/prodapi)\n\nA thin layer on top of [FastAPI](https://fastapi.tiangolo.com/) with the following features:\n\n- Integrates with [FastAPI-Security](https://jmagnusson.github.io/fastapi-security/) to add a custom route `/users/me` (path is overridable)\n- Easily add CORS to your app by calling `app.with_basic_cors()`\n- Add health routes to the app via `app.with_health_routes()`. Adds a liveness route at `/__is-alive` and a readiness route at `/__is-ready` (both paths can be overridden). Useful together with [Kubernetes liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) for example.\n- And, thanks to FastAPI, all routes are automatically added to the API documentation\n\n## Installation\n\n```\npip install prodapi\n```\n\n## Example\n\n```python\nfrom prodapi import ProdAPI, ApiRouter, FastAPISecurity\n\n# First let\'s set up security, via FastAPI-Security\n\nsecurity = FastAPISecurity()\n\n# Set up HTTP Basic Auth\nsecurity.init_basic_auth([\n    {"username": "johndoe", "password": "123"},\n    {"username": "janedoe", "password": "abc123"},\n])\n\n# Set up OAuth2 and OIDC\n# NOTE: There is also `init_oauth2_through_jwks` in case OIDC is not available\nsecurity.init_oauth2_through_oidc(\n    "https://my-auth0-tenant.eu.auth0.com/.well-known/openid-configuration",\n)\n\n# Make sure that basic auth user `jane` and OAuth2 user\n# `p56OnzZb8KrWC9paxCyv8ylyB2flTIky@clients` gets all permissions automatically.\n# NOTE: For basic auth you have to set up permissions this way, for OAuth2 permissions\n#       will be automatically extracted from the incoming JWT token (via the key\n#       `permissions`, which might only be implemented for Auth0)\nsecurity.add_permission_overrides({\n    "jane": ["*"],\n    "p56OnzZb8KrWC9paxCyv8ylyB2flTIky@clients": ["*"],\n)\n\n# Now we\'re ready to create the app\n# NOTE: ProdAPI is just a thin layer on top of `fastapi.FastAPI`\napp = ProdAPI()\n\n# CORS - Allow any origins, methods and headers. Don\'t expose any headers.\napp.with_basic_cors()\n\n# Add routes `/__is-alive` and `/__is-ready`. Useful together with Kubernetes or similar\n# URL paths are configurable.\napp.with_health_routes()\n\n# Enable `/users/me` route to get info about the user. URL path is configurable.\napp.with_user_routes(security)\n\n# Create our app specific API router and our routes\nproducts_router = ApiRouter()\n\n@products_router.get("/products")\ndef list_products():\n    return []\n\napp.include_router(products_router)\n\n# And we\'re done! Now just use uvicorn or similar to deploy.\n\n```\n\n## TODO\n1. Create cli utility (using [tiangolo typer](https://github.com/tiangolo/typer)?), which can generate:\n    1. A stub project using `prodapi`\n    1. Frontend (React?)\n    1. docker-compose.yml and Dockerfile\n    1. Kubernetes deployment files\n',
    'author': 'Jacob Magnusson',
    'author_email': 'm@jacobian.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://jmagnusson.github.io/prodapi/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
