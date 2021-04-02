# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spoqa_requests_backoff']
install_requires = \
['backoff>=1.10.0,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'spoqa-requests-backoff',
    'version': '0.1.1',
    'description': 'Backoff Session for requests',
    'long_description': "# spoqa-requests-backoff\n\n[![MIT License](https://badgen.net/badge/license/MIT/cyan)](LICENSE)\n[![PyPI](https://badgen.net/pypi/v/spoqa-requests-backoff)](https://pypi.org/project/spoqa-requests-backoff/)\n\nBackoff session for requests\n\n## Usage\n\n```python\nresp = BackoffSession().get('https://...')\n```\n\nBy default, `BackoffSession` tries before giving up until any following condition is met:\n\n- Tries 10 times\n- Reaches 20 seconds\n- Meets `requests.RequestException`\n- Meets HTTP client error (4xx)\n\nBehaviors above can be customized with parameters.\n\n```python\nBackoffSession(\n    exception=(RequestException, ValueError),  # Give up when ValueError occurs, too.\n    max_tries=100,  # Tries 100 times before giving up\n    max_time=300,  # Wait until maximum 300 seconds before giving up\n    giveup=lambda e: e.response.text == 'You're fired!'  # Give up when specific response is met\n)\n```\n\nBackoffSession heavily depends on [`backoff`](https://github.com/litl/backoff) package.\n\n## License\n\n_spoqa-requests-backoff_ is distributed under the terms of MIT License.\n\nSee [LICENSE](LICENSE) for more details.\n",
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
