# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['copier_templates_extensions', 'copier_templates_extensions.extensions']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['copier-templates-extensions = '
                     'copier_templates_extensions.cli:main']}

setup_kwargs = {
    'name': 'copier-templates-extensions',
    'version': '0.1.1',
    'description': 'Special Jinja2 extension for Copier that allows to load extensions using file paths relative to the template root instead of Python dotted paths.',
    'long_description': '# Copier Templates Extensions\n\n[![ci](https://github.com/pawamoy/copier-templates-extensions/workflows/ci/badge.svg)](https://github.com/pawamoy/copier-templates-extensions/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/copier-templates-extensions/)\n[![pypi version](https://img.shields.io/pypi/v/copier-templates-extensions.svg)](https://pypi.org/project/copier-templates-extensions/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/copier-templates-extensions/community)\n\nSpecial Jinja2 extension for Copier that allows to load extensions using file paths relative to the template root instead of Python dotted paths.\n\n## Requirements\n\nCopier Templates Extensions requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n\n## Installation\n\nWith `pip`:\n```bash\npip install copier-templates-extensions\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npip install --user pipx\n\npipx install copier\npipx inject copier copier-templates-extensions\n```\n\n## Usage\n\nIn your template configuration,\nfirst add our loader extension,\nthen add your templates extensions\nusing relative file paths,\nand the class name after a colon:\n\n```yaml\n_extensions:\n- copier_templates_extensions.TemplateExtensionLoader\n- extensions/context.py:ContextUpdater\n- extensions/slugify.py:SlugifyExtension\n```\n\n### Context hook extension\n\nThis package also provides a convenient extension class\nallowing template writers to update the context used\nto render templates, in order to add, modify or remove\nitems of the context.\n\nIn one of your relative path extensions modules,\ncreate a class that inherits from `ContextHook`,\nand override its `hook` method:\n\n```python\nfrom copier_templates_extensions import ContextHook\n\n\nclass ContextUpdater(ContextHook):\n    def hook(self, context):\n        new_context = {}\n        new_context["say"] = "hello " + context["name"]\n        return new_context\n```\n\nUsing the above example, your context will be updated\nwith the `new_context` returned by the method.\nIf you prefer to modify the context in-place instead,\nfor example to *remove* items from it,\nset the `update` class attribute to `False`:\n\n```python\nfrom copier_templates_extensions import ContextHook\n\n\nclass ContextUpdater(ContextHook):\n    update = False\n\n    def hook(self, context):\n        context["say"] = "hello " + context["name"]\n        del context["name"]\n```\n\n## How does it work?\n\nBeware the ugly hack!\nUpon loading the special *loader* extension,\nthe function responsible for importing\na Python object using its dotted-path (a string)\nis patched in the `jinja.environment` module,\nwhere it\'s used to load extensions.\nThe patched version adds support\nfor loading extensions using relative file paths.\nThe file system loader of the Jinja environment\nand its `searchpaths` attribute are used to\nfind the local clone of the template and determine\nthe absolute path of the extensions to load.',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pawamoy/copier-templates-extensions',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<3.10',
}


setup(**setup_kwargs)
