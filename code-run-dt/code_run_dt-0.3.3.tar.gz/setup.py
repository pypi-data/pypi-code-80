# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['code_run_dt', 'code_run_dt.report', 'code_run_dt.task_config']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7,<2.0']

setup_kwargs = {
    'name': 'code-run-dt',
    'version': '0.3.3',
    'description': '编程乐园类型定义',
    'long_description': '# code run data type\n\nCode Run Data Definition\n\n## WARNING\n\n    may useless to you\n\n[在线运行代码工具](https://run.c-art.tech/)\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://run.c-art.tech/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
