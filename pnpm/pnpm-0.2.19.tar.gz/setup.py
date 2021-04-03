# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pnpm', 'pnpm.generator.__pkg__']

package_data = \
{'': ['*'],
 'pnpm': ['generator/docs/*'],
 'pnpm.generator.__pkg__': ['.icona/*',
                            '.icona/.git/*',
                            '.icona/.git/hooks/*',
                            '.icona/.git/info/*',
                            '.icona/.git/logs/*',
                            '.icona/.git/logs/refs/heads/*',
                            '.icona/.git/logs/refs/remotes/origin/*',
                            '.icona/.git/objects/pack/*',
                            '.icona/.git/refs/heads/*',
                            '.icona/.git/refs/remotes/origin/*',
                            'dist/*',
                            'docs/*',
                            'docs/scripts/*',
                            'src/*',
                            'src/.build_assets/*',
                            'src/icons/*',
                            'src/styles/*',
                            'test/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'numpy>=1.20.1,<2.0.0',
 'rglob>=1.7,<2.0',
 'rich>=9.13.0,<10.0.0']

setup_kwargs = {
    'name': 'pnpm',
    'version': '0.2.19',
    'description': '',
    'long_description': None,
    'author': 'robo-monk',
    'author_email': 'rrobomonk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
