# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['molecule_k3d', 'molecule_k3d.test']

package_data = \
{'': ['*'],
 'molecule_k3d': ['cookiecutter/*',
                  'cookiecutter/{{cookiecutter.molecule_directory}}/{{cookiecutter.scenario_name}}/*',
                  'playbooks/*']}

entry_points = \
{'molecule.driver': ['k3d = molecule_k3d.driver:K3d']}

setup_kwargs = {
    'name': 'molecule-k3d',
    'version': '0.1.0',
    'description': 'molecule-k3d - Molecule K3D Driver allows Molecule users to test Ansible code using K3D.',
    'long_description': '# molecule-k3d\n\nmolecule-k3d - Molecule K3D Driver allows Molecule users to test Ansible code using K3D.\n\n## Testing\n\nTo execute unit tests.\n\n    $ make dep\n    $ make test\n\n## License\n\nThe [MIT] License.\n\n[MIT]: LICENSE\n',
    'author': 'John Dewey',
    'author_email': 'john@dewey.ws',
    'maintainer': 'John Dewey',
    'maintainer_email': 'john@dewey.ws',
    'url': 'https://github.com/retr0h/molecule-k3d',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
