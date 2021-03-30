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
 'tess-cloud>=0.2.1',
 'tess-point>=0.6.1',
 'tqdm>=4.51']

setup_kwargs = {
    'name': 'tess-locator',
    'version': '0.4.1',
    'description': 'Fast offline queries of TESS FFI positions and filenames.',
    'long_description': 'tess-locator\n============\n\n**Where is my favorite star or galaxy in NASA\'s TESS Full Frame Image data set?**\n\n|pypi| |pytest| |black| |flake8| |mypy|\n\n.. |pypi| image:: https://img.shields.io/pypi/v/tess-locator\n                :target: https://pypi.python.org/pypi/tess-locator\n.. |pytest| image:: https://github.com/SSDataLab/tess-locator/workflows/pytest/badge.svg\n.. |black| image:: https://github.com/SSDataLab/tess-locator/workflows/black/badge.svg\n.. |flake8| image:: https://github.com/SSDataLab/tess-locator/workflows/flake8/badge.svg\n.. |mypy| image:: https://github.com/SSDataLab/tess-locator/workflows/mypy/badge.svg\n\n\n`tess-locator` is a user-friendly package which combines the\n`tess-point <https://github.com/christopherburke/tess-point>`_\nand `tess-cloud <https://github.com/SSDataLab/tess-cloud>`_ packages\nto enable the positions of astronomical objects in the TESS data set\nto be queried in a fast and friendly way.\n\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    python -m pip install tess-locator\n\nExample use\n-----------\n\nConverting celestial coordinates to TESS pixel coordinates:\n\n.. code-block:: python\n\n    >>> from tess_locator import locate\n    >>> locate("Alpha Cen")\n    List of 3 coordinates\n    ↳[TessCoord(sector=11, camera=2, ccd=2, column=1699.1, row=1860.3, time=None)\n      TessCoord(sector=12, camera=2, ccd=1, column=359.9, row=1838.7, time=None)\n      TessCoord(sector=38, camera=2, ccd=2, column=941.1, row=1953.7, time=None)]\n\n\nObtaining pixel coordinates for a specific time:\n\n.. code-block:: python\n\n    >>> locate("Alpha Cen", time="2019-04-28")\n    List of 1 coordinates\n    ↳[TessCoord(sector=11, camera=2, ccd=2, column=1699.1, row=1860.3, time=2019-04-28 00:00:00)]\n\n\nObtaining pixel coordinates for a specific celestial coordinate:\n\n.. code-block:: python\n\n    >>> from astropy.coordinates import SkyCoord\n    >>> crd = SkyCoord(ra=60, dec=70, unit=\'deg\')\n    >>> locate(crd)\n    List of 1 coordinates\n    ↳[TessCoord(sector=19, camera=2, ccd=2, column=355.3, row=1045.9, time=None)]\n\n\nYou can access the properties of `TessCoord` objects using standard list and attribute syntax:\n\n.. code-block:: python\n\n    >>> crdlist = locate("Alpha Cen")\n    >>> crdlist[0].sector, crdlist[0].camera, crdlist[0].ccd, crdlist[0].column, crdlist[0].row\n    (11, 2, 2, 1699.0540739785683, 1860.2510951146114)\n\n\nWhen you have obtained a `TessCoord` object, you can use it to obtain a list of the TESS Full Frame Images (FFIs) which covered the position:\n\n.. code-block:: python\n\n    >>> crdlist[0].list_images()\n    List of 1248 images\n    ↳[TessImage("tess2019113062933-s0011-2-2-0143-s_ffic.fits")\n      TessImage("tess2019113065933-s0011-2-2-0143-s_ffic.fits")\n      TessImage("tess2019113072933-s0011-2-2-0143-s_ffic.fits")\n      TessImage("tess2019113075933-s0011-2-2-0143-s_ffic.fits")\n      ...\n      TessImage("tess2019140065932-s0011-2-2-0143-s_ffic.fits")\n      TessImage("tess2019140072932-s0011-2-2-0143-s_ffic.fits")\n      TessImage("tess2019140075932-s0011-2-2-0143-s_ffic.fits")\n      TessImage("tess2019140082932-s0011-2-2-0143-s_ffic.fits")]\n\n\n\nDocumentation\n-------------\n\nPlease visit the `tutorial <https://github.com/SSDataLab/tess-locator/blob/master/docs/tutorial.ipynb>`_.\n\n\nSimilar packages\n----------------\n\n* `tess-point <https://github.com/christopherburke/tess-point>`_ is the package being called behind the scenes. Compared to `tess-point`, we add a user-friendly API and the ability to specify the time, which is important for moving objects.\n* `astroquery.mast <https://astroquery.readthedocs.io/en/latest/mast/mast.html>`_ includes the excellent ``TesscutClass.get_sectors()`` method which queries a web API. This package provides an offline version of that service, and adds the ability to query by time.\n* `tess-waldo <https://github.com/SimonJMurphy/tess-waldo>`_ lets you visualize how a target moves over the detector across sectors. It queries the ``TessCut`` service to obtain this information. This package adds the ability to create such plots offline.\n',
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
