# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dependable']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'dependable',
    'version': '0.1.0',
    'description': 'Dependency injection system extracted from FastAPI',
    'long_description': '<h1 align="center">\n    <strong>dependable</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/dmtrs/dependable" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/dmtrs/dependable" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/dmtrs/dependable/Test">\n        <img src="https://img.shields.io/codecov/c/github/dmtrs/dependable">\n    <br />\n    <a href="https://pypi.org/project/dependable" target="_blank">\n        <img src="https://img.shields.io/pypi/v/dependable" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/dependable">\n    <img src="https://img.shields.io/github/license/dmtrs/dependable">\n</p>\n\nDependency injection system extracted from `fastapi`\n\n```python\nimport asyncio\nfrom random import random\n\nfrom dependable import dependant, Depends\n\n@dependant\nasync def main(*, choice: int = Depends(random)) -> None:\n    print(choice)\n\nasyncio.run(main())\n```\n\nMore on [examples](examples/tick.py)\n\n## Installation\n\n``` bash\npoetry add dependable # pip install dependable\n```\n\n## Python 3.6\n\n- Backport require of [async-exit-stack](https://pypi.org/project/async-exit-stack/) and [async_generator](https://pypi.org/project/async_generator/)\n```bash\npoetry add async-exit-stack async_generator # pip install async-exit-stack async_generator\n```\n\n## Development\n\n```bash\ndocker build -t dependable .\n```\n\n```bash\ndocker run --rm -v $(pwd):/usr/src/app dependable scripts/dev\n```\n\n## References\n\n- [tiangolo/fastapi#2967](https://github.com/tiangolo/fastapi/issues/2967)\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Dimitrios Flaco Mengidis ',
    'author_email': 'tydeas.dr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmtrs/dependable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
