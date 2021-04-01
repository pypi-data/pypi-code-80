# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'data_grid_surface'}

packages = \
['config',
 'data_grid_surface',
 'data_grid_surface.config',
 'data_grid_surface.services']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'data-grid-surface',
    'version': '1.0.0',
    'description': 'SDK to communicate with data-grid API',
    'long_description': "\n# DATA-GRID-SURFACE\nSDK to communicate with data-grid API service.\nIt uses the API service and it's end-points to determine if the given emails or passwords have been compromised.\n\n\n## Installation\n\nInstall data-grid-surface SDK:\n\n```\npip install data-grid-surface\n```\n\n## Using data-grid-access sdk\n\nImport DataGrid class from library\n\n```\nfrom data_grid_surface.data_grid import DataGrid\n```\n\nYou will need to provide username and password parameters to DataGrid class constructor. These are credentials for data-grid API service.\n\n### DataGrid methods\n\nDataGrid methods return dictionary as a result.\n\n**Methods:**\n* check_email(email) -> email as string parameter\n* check_password(password) -> password as string parameter\n\n**Use example:**\n\n```\nfrom data_grid_surface.data_grid import DataGrid\n\ndataGrid = DataGrid(username='testuser', password='testpassword')\nresponse = dataGrid.checkEmail('email@example.com')\nprint(response)\n```\n\n**Response examples:**\n\n```\n{\n    'status': 'success', \n    'data': {\n        'emails': [\n            {\n                '_id': '6033927de534be1225cd4052', \n                'email': 'email@example.com'\n            }\n        ]\n    }\n}\n```\n\n```\n{\n    'status': 'fail', \n    'message': 'Not Found'\n}\n```",
    'author': 'Marko Latinovic',
    'author_email': 'marko.latinovic@bluegrid.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': '',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
