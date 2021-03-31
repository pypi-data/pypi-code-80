# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hotmodern_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'marshmallow>=3.10.0,<4.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['hotmodern-python = hotmodern_python.console:main']}

setup_kwargs = {
    'name': 'hotmodern-python',
    'version': '0.1.1',
    'description': "Python learning project by blog posts series 'Hypermodern Python' (by Claudio Jolowicz)",
    'long_description': '[![Tests](https://github.com/hotenov/hotmodern-python/actions/workflows/tests.yml/badge.svg)](https://github.com/hotenov/hotmodern-python/actions/workflows/tests.yml)\n[![codecov.io](https://codecov.io/github/hotenov/hotmodern-python/coverage.svg?branch=main)](https://codecov.io/github/hotenov/hotmodern-python/coverage.svg?branch=main)\n[![Docs](https://readthedocs.org/projects/hotmodern-python/badge/?version=latest)](https://hotmodern-python.readthedocs.io/en/latest/?badge=latest)\n\n\n# hotmodern-python\n\nMy Python learning project by article series \'[Hypermodern Python](https://cjolowicz.github.io/posts/)\' (by [Claudio Jolowicz](https://github.com/cjolowicz))\n\nThis repo 98% repeats code from these articles\nwith little improvements for Windows environment\nand except several components\n(pre-commit, typeguard)\n\n## Notes for Windows host\n\n### Functions with temp file on Windows\n\nWindows has security limitation for temp files:\nOS does not allow processes other than the one used to create the NamedTemporaryFile to access the file\n([from here](https://github.com/bravoserver/bravo/issues/111#issuecomment-826990))\n\nThat\'s why I modified code like this:\n\n```python\n# noxfile.py\nimport pathlib\n\ndef install_with_constraints(session: Session, *args: str, **kwargs: Any) -> None:\n    """Install packages constrained by Poetry\'s lock file."""\n    with tempfile.NamedTemporaryFile(delete=False) as requirements:\n        session.run(\n            "poetry",\n            "export",\n            ...\n        )\n        session.install(f"--constraint={requirements.name}", *args, **kwargs)\n    pathlib.Path(requirements.name).unlink()\n```\n\n### Run Nox sessions with pyenv\'s Python versions\n\n#### Option A\n\nUse Nox CLI argument `--extra-pythons` and full paths to desired version of Python interpreter\n\nExample:\n\n```powershell\nnox --extra-pythons "C:\\users\\winfan\\.pyenv\\pyenv-win\\versions\\3.8.2\\python.exe" "C:\\users\\winfan\\.pyenv\\pyenv-win\\versions\\3.9.2\\python.exe"\n```\n\nwill run all sessions with Python specified in noxfile.py _(or skip if not found)_\nand with all Pythons passed in this command.\nSee [detailed explanation](https://github.com/theacodes/nox/issues/412#issuecomment-810425155) how `--extra-pythons` and `--extra-python` works from Claudio Jolowicz himself\n\n#### Option B\n\nCreate separate noxfile for local execution.\nDuplicate all sessions and change python versions like this:\n\n```python\n# noxfile.local.py\n\n@nox.session(\n    python=[\n        r"C:\\users\\winfan\\.pyenv\\pyenv-win\\versions\\3.8.2\\python.exe",\n        r"C:\\users\\winfan\\.pyenv\\pyenv-win\\versions\\3.9.2\\python.exe",\n    ],\n    reuse_venv=True,\n)\n```\n\nThen run command in your Terminal `nox -f noxfile.local.py`  \nDon\'t forget to add this file to `.gitignore`\n',
    'author': 'Artem Hotenov',
    'author_email': 'artem@hotenov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hotenov/hotmodern-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
