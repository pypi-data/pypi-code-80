# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['filterflow']

package_data = \
{'': ['*']}

install_requires = \
['plotly>=4.14.3,<5.0.0']

setup_kwargs = {
    'name': 'filterflow',
    'version': '0.1.0',
    'description': 'A library to create data flow charts.',
    'long_description': '# filterflow\n\nThis package allows for the creation of funnel graphs\nto quickly and easily display the length of a dataset\nas a series of data processing steps are applied to it.\n\n## Example usage\n\n```\nfrom filterflow import Flow, FlowElement\n\n# Create list from 0 to 100\nelements = range(100)\n\n# Declare flow\nf = Flow("Example with filtering numbers", len(elements))\n\n# Filter out odd numbers\nevens_only = [x for x in elements if x%2 == 0]\nf.add_step("Removing odd numbers gives:", len(evens_only))\n\n# Filter out numbers greater than 40\nevens_less_than_40 = [x for x in elements if x < 40]\nf.add_step("Removing numbers >= 40:", len(evens_less_than_40))\n\n# Plot chart\nf.plot()\n```\n\n![\'Example image\'](https://github.com/LeviWadd/filterflow/raw/master/images/example.JPG)',
    'author': 'Levi Waddingham',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
