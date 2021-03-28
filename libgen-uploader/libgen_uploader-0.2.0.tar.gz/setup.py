# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libgen_uploader']

package_data = \
{'': ['*']}

install_requires = \
['Cerberus>=1.3.2,<2.0.0', 'returns==0.16.0', 'robobrowser>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'libgen-uploader',
    'version': '0.2.0',
    'description': 'A Library Genesis ebook uploader',
    'long_description': '_A Library Genesis ebook uploader._\n\n**This library is to be considered unstable/beta until v1.0.0. API may change until then.**\n\n## Installation\n\n```bash\npip install libgen-uploader\n```\n\n## Usage from command-line\n\n```bash\npython -m libgen_uploader (--scitech|--fiction) [args] book.epub\n```\n\nOptional arguments:\n```\n--metadata-source {local,amazon_us,amazon_uk,amazon_de,amazon_fr,amazon_it,amazon_es,amazon_jp,bl,douban,goodreads,google_books,loc,rsl,worldcat}\n    Source to fetch book metadata from\n\n--metadata-query METADATA_QUERY\n    Metadata query for selected source (supports multiple, comma-separated)\n\n-d, --debug\n    Activate debug logging\n```\n\n## Usage as library\n\nThis library uses [returns](https://github.com/dry-python/returns), and returns [Result containers](https://returns.readthedocs.io/en/latest/pages/result.html) which can either contain a success value or a failure/exception. Exception values are returned, not raised, so you can handle them as you wish and avoid wide `try/except` blocks or program crashes due to unforeseen exceptions.\n\n### Uploading books\n\nTwo methods are exposed for uploading books: `upload_scitech` and `upload_fiction`.\n\n```python\nfrom libgen_uploader import LibgenUploader\nfrom returns.pipeline import is_successful\n\nu = LibgenUploader()\n\nresult = u.upload_fiction("book.epub")\nif is_successful(result):\n    upload_url = result.unwrap() # type: str\nelse:\n    failure = result.failure() # type: Exception\n```\n\n### Fetching metadata\n\nMetadata support is not complete yet. The default metadata are the one contained in the book itself. You can then fetch additional metadata from the sources supported by the Library Genesis upload form, namely:\n\n- Other Library Genesis record (`"local"`)\n- Amazon US/UK/DE/FR/IT/ES/JP (`"amazon_us"`, `"amazon_uk"`, `"amazon_de"`, `"amazon_fr"`, `"amazon_it"`, `"amazon_es"`, `"amazon_jp"`)\n- British Library (`"bl"`)\n- Douban.com (`"douban"`)\n- Goodreads (`"goodreads"`)\n- Google Books (`"google_books"`)\n- Library of Congress (`"loc"`)\n- Russian State Library (`"rsl"`)\n- WorldCat (`"worldcat"`)\n\nAny fetched metadata completely replaces all metadata contained in the ebook itself (this is how the upload form works), and any custom (user-provided) metadata overrides the default/fetched ones.\n\n```python\n# use metadata contained in the book\nu = LibgenUploader()\nu.upload_scitech("book.epub")\n\n# session-wide metadata source\nu = LibgenUploader(metadata_source="amazon_it")\nu.upload_scitech("book.epub", metadata_query="9788812312312")\n\n# book-level metadata source\nu = LibgenUploader()\nu.upload_scitech(\n    "book.epub",\n    metadata_source="amazon_it",\n    metadata_query=["9788812312312", "another_isbn"] # you can pass an array of values in case the first ones don\'t return results\n)\n\n# custom, user-provided metadata (override default/fetched)\nfrom libgen_uploader import LibgenMetadata\n\nm = LibgenMetadata(title="new title", authors=["John Smith", "Jack Black"])\nu.upload_scitech("book.epub", metadata=m)\n```',
    'author': 'Francesco Truzzi',
    'author_email': 'francesco@truzzi.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ftruzzi/libgen_uploader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
