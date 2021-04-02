# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asy']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'asy',
    'version': '0.0.3',
    'description': '',
    'long_description': '# asy\n[![Version](https://img.shields.io/pypi/v/asy)](https://pypi.org/project/asy)\n[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n`asy` is easy and powerful for `asyncio`.\n\n# Motivation for development\n\n- Simple cancellation\n- Improve the coordination of async functions between libraries\n- No more programs for execution management\n- Develop specifications like ASGI\n\n\n# Installation\n\n``` shell\npip install asy\n```\n\n# Getting started\n\nCreate deamons, in `example.py`:\n\n``` python\nimport asyncio\n\n# cancelable limited loop\nasync def func1(token):\n    for i in range(10):\n        if token.is_cancelled:\n            break\n        print("waiting")\n        await asyncio.sleep(1)\n    print("complete func2.")\n\n# cancelable infinity loop\nasync def func2():\n    while True:\n        print("waiting")\n        await asyncio.sleep(1)\n\n# uncancelable limited loop\ndef func3():\n    for i in range(1000):\n        print(i)\n\n# from callable\nclass YourDeamon:\n    async def __call__(self, token):\n        while not token.is_cancelled:\n            await asyncio.sleep(1)\n        print("complete.")\n\nfunc4 = YourDeamon()\n\n\n# Do not run\n# infinity loop\n# async def func5()):\n#     while True:\n#         print("waiting")\n```\n\nRun in shell.\n\n``` shell\npython3 -m asy example:func1 example:func2 example:func3 example:func4\n```\n\nRun in Python script.\n\n``` python\nimport asy\nfrom example import func1, func2, func3, func4\n\nsupervisor = asy.supervise(func1, func2, func3, func4)\nsupervisor.run()\n\n# or\nasy.run(func1, func2, func3, func4)\n```\n\n\nLet\'s end the daemon with `Ctrl-C` and enjoy `asy`!\n\n# Caution\n`asy` is a beta version. Please do not use it in production.\n',
    'author': 'sasano8',
    'author_email': 'y-sasahara@ys-method.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
