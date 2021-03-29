# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tess_locator']

package_data = \
{'': ['*'], 'tess_locator': ['data/*']}

install_requires = \
['astropy>=4.0',
 'attrs>=20.3.0',
 'numpy>=1.19',
 'pandas>=1.0',
 'tess-cloud>=0.2.0',
 'tess-point>=0.6.1',
 'tqdm>=4.51']

setup_kwargs = {
    'name': 'tess-locator',
    'version': '0.4.0',
    'description': 'Fast offline queries of TESS FFI positions and filenames.',
    'long_description': 'tess-locator\n============\n\n**Where is my favorite star or galaxy in NASA\'s TESS Full Frame Image data set?**\n\n|pypi| |pytest| |black| |flake8| |mypy|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/tess-locator\n                :target: https://pypi.python.org/pypi/tess-locator\n.. |pytest| image:: https://github.com/SSDataLab/tess-locator/workflows/pytest/badge.svg\n.. |black| image:: https://github.com/SSDataLab/tess-locator/workflows/black/badge.svg\n.. |flake8| image:: https://github.com/SSDataLab/tess-locator/workflows/flake8/badge.svg\n.. |mypy| image:: https://github.com/SSDataLab/tess-locator/workflows/mypy/badge.svg\n\n\n`tess-locator` is a user-friendly wrapper around the `tess-point <https://github.com/christopherburke/tess-point>`_\npackage which allows the positions of astronomical objects in the TESS data set\nto be queried in a fast and friendly way.\n\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    python -m pip install tess-locator\n\nExample use\n-----------\n\nConverting celestial to pixel coordinates:\n\n.. code-block:: python\n\n    >>> from tess_locator import locate\n    >>> locate("Alpha Cen")\n    List of 3 coordinates\n    ↳[TessCoord(sector=11, camera=2, ccd=2, column=1699.1, row=1860.3, time=None)\n      TessCoord(sector=12, camera=2, ccd=1, column=359.9, row=1838.7, time=None)\n      TessCoord(sector=38, camera=2, ccd=2, column=941.1, row=1953.7, time=None)]\n\n\nObtaining pixel coordinates for a specific time:\n\n.. code-block:: python\n\n    >>> locate("Alpha Cen", time="2019-04-28")\n    List of 1 coordinates\n    ↳[TessCoord(sector=11, camera=2, ccd=2, column=1699.1, row=1860.3, time=2019-04-28 00:00:00)]\n\n\nDocumentation\n-------------\n\nPlease visit the `tutorial <https://github.com/SSDataLab/tess-locator/blob/master/docs/tutorial.ipynb>`_.\n\n\nSimilar packages\n----------------\n\n* `tess-point <https://github.com/christopherburke/tess-point>`_ is the package being called behind the scenes. Compared to `tess-point`, we add a user-friendly API and the ability to specify the time, which is important for moving objects.\n* `astroquery.mast <https://astroquery.readthedocs.io/en/latest/mast/mast.html>`_ includes the excellent ``TesscutClass.get_sectors()`` method which queries a web API. This package provides an offline version of that service, and adds the ability to query by time.\n* `tess-waldo <https://github.com/SimonJMurphy/tess-waldo>`_ lets you visualize how a target moves over the detector across sectors. It queries the ``TessCut`` service to obtain this information. This package adds the ability to create such plots offline.\n',
    'author': 'Geert Barentsen',
    'author_email': 'hello@geert.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SSDataLab/tess-locator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
