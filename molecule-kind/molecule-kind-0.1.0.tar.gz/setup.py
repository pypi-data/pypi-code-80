# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['molecule_kind', 'molecule_kind.test']

package_data = \
{'': ['*'],
 'molecule_kind': ['cookiecutter/*',
                   'cookiecutter/{{cookiecutter.molecule_directory}}/{{cookiecutter.scenario_name}}/*']}

entry_points = \
{'molecule.driver': ['kind = molecule_kind.driver:Kind']}

setup_kwargs = {
    'name': 'molecule-kind',
    'version': '0.1.0',
    'description': 'molecule-kind - Molecule Kind Driver allows Molecule users to test Ansible code using Kind.',
    'long_description': '# molecule-kind\n\n[![Unit Test](https://github.com/retr0h/molecule-kind/actions/workflows/unit.yml/badge.svg)](https://github.com/retr0h/molecule-kind/actions/workflows/unit.yml)\n[![Lint](https://github.com/retr0h/molecule-kind/actions/workflows/lint.yml/badge.svg)](https://github.com/retr0h/molecule-kind/actions/workflows/lint.yml)\n\nmolecule-kind - Molecule Kind Driver allows Molecule users to test Ansible code using Kind.\n\n## Dependencies\n\n* [kind][]\n\n## Installing\n\n    $ pip install molecule-kind\n\n## Usage\n\n    $ molecule init scenario -d kind\n    $ molecule test\n\n## Testing\n\nTo execute unit tests.\n\n    $ make dep\n    $ make test\n\n## License\n\nThe [MIT] License.\n\n[kind]: https://github.com/kubernetes-sigs/kind\n[MIT]: LICENSE\n',
    'author': 'John Dewey',
    'author_email': 'john@dewey.ws',
    'maintainer': 'John Dewey',
    'maintainer_email': 'john@dewey.ws',
    'url': 'https://github.com/retr0h/molecule-kind',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
