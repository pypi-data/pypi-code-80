# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spoqa_requests_backoff']
install_requires = \
['backoff>=1.10.0,<2.0.0',
 'backports.functools_lru_cache!=1.6.2,!=1.6.3',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'spoqa-requests-backoff',
    'version': '0.1.0',
    'description': 'Backoff Session for requests',
    'long_description': "# spoqa-requests-backoff\n\nBackoff session for requests\n\n## Usage\n\nBy default, `BackoffSession` \n\n```python\nresp = BackoffSession().get('https://...')\n```\n\n## License\n\n_spoqa-requests-backoff_ is distributed under the terms of MIT License.\n\nSee [LICENSE](LICENSE) for more details.\n",
    'author': 'Spoqa Creators',
    'author_email': 'dev@spoqa.com',
    'maintainer': 'rusty',
    'maintainer_email': 'rusty@spoqa.com',
    'url': 'https://github.com/spoqa/requests-backoff',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
