# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expool']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'expool',
    'version': '0.1.0',
    'description': 'Simple asynchronous execution pool primitive for Python 3.6+',
    'long_description': "# Expool\n[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)\n[![Build Status](https://travis-ci.com/scanfactory/execution-pool.svg?branch=master)](https://travis-ci.com/scanfactory/execution-pool)\n[![codecov](https://codecov.io/gh/scanfactory/execution-pool/branch/master/graph/badge.svg)](https://app.codecov.io/gh/scanfactory/execution-pool)\n\nSimple asynchronous execution pool primitive.\nYou can think of it as of a `threading.ThreadPool` for coroutines.\n\n## Usage\n```python\nimport asyncio\nfrom expool import ExecutionPoolSimple\n\nasync def main():\n    pool = ExecutionPoolSimple(size=3) # size parameter sets the max amount of concurrent coroutines \n    \n    async def some_job():\n        await asyncio.sleep(3)\n    \n    await pool.add(some_job) # Returns immediately if the pool is not full.\n    await pool.add(some_job) # If the pool max size is reached, waits \n    # until one of the pool's coroutines finishes.\n    \n    await pool.close()  # wait for all of the jobs to finish.\n```\n\nYou may also set a timeout for `.close()` method:\n```python\n    await pool.close(timeout=10)  \n```\nIf the timeout is reached, `ExecutionPoolSimple` cancels all remaining coroutines and returns.\n\nYou may also want to check out `ExecutionPool` decorators:\n- `ExecutionPoolMonitored` - a pool with periodical logging of the jobs inside the pool;\n- `ExecutionPoolCapped` - a pool with a limited lifespan.\n\nInstallation\n```shell\npip install expool\n```\n",
    'author': 'monomonedula',
    'author_email': 'valh@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scanfactory/execution-pool',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
