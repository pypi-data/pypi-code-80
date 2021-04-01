# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lrphase']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.78,<2.0',
 'pyliftover>=0.4,<0.5',
 'pysam>=0.16.0,<0.17.0',
 'requests>=2.25.1,<3.0.0',
 'ssw>=0.4.1,<0.5.0',
 'typer-cli>=0.0.11,<0.0.12',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['LRphase = lrphase.cli:run']}

setup_kwargs = {
    'name': 'lrphase',
    'version': '0.4.1',
    'description': 'Phase individual long reads with haplotype information',
    'long_description': None,
    'author': 'Greg Farnum',
    'author_email': 'gregfar@umich.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
