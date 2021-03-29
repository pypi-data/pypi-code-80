# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.26,<2.0.0',
 'fastparquet>=0.3.3,<0.5.0',
 'pandas>=0.23.3,<2.0.0',
 'psycopg2>=2.8.6,<3.0.0',
 'pyarrow>=0.16.0,<0.17.0',
 'xlrd>=1.2.0,<2.0.0',
 'xlsxwriter>=1.2.8,<2.0.0']

setup_kwargs = {
    'name': 'pandas-aws',
    'version': '0.1.6',
    'description': '',
    'long_description': "[![Build Status](https://travis-ci.com/FlorentPajot/pandas-aws.svg?branch=master)](https://travis-ci.com/FlorentPajot/pandas-aws) [![codecov](https://codecov.io/gh/FlorentPajot/pandas-aws/branch/master/graph/badge.svg)](https://codecov.io/gh/FlorentPajot/pandas-aws)\n\n# Pandas AWS - AWS made easy for data scientists\n\nPandas AWS makes it super easy to use a pandas.DataFrame along with AWS services.\n\n## Working with S3\n\nFirst create an S3 client to be used later and define a bucket\n```\nfrom pandas_aws import get_client\n\ns3 = get_client('s3')\nMY_BUCKET= 'pandas-aws-bucket'\n```\nExample 1: get a DataFrame from a parquet file stored in S3\n```\nfrom pandas_aws.s3 import get_df\n\ndf_from_parquet_file = get_df(s3, MY_BUCKET, 'my_parquet_file_path', format='parquet')\n```\nExample 2: get a DataFrame from multiple CSV files (with same schema) stored in S3\n```\nfrom pandas_aws.s3 import get_df_from_keys\n\ndf_from_list = get_df_from_keys(s3, MY_BUCKET, prefix='my-folder', suffix='.csv')\n```\nExample 3: put a DataFrame into S3 using an xlsx (Excel) file format\n```\nfrom pandas_aws.s3 import put_df\n\nput_df(s3, my_dataframe, MY_BUCKET, 'target_file_path', format='xlsx')\n```\nExample 4: put a DataFrame into S3 using multi parts upload\n```\nfrom pandas_aws.s3 import put_df\n\nput_df(s3, my_dataframe, MY_BUCKET, 'target_file_path', format='csv', compression='gzip', parts=8)\n```\n\n# Installing pandas-aws\n\n## Pip installation\n\nYou can use pip to download the package\n\n`pip install pandas-aws`\n\n# Contributing to pandas-aws\n\n## Git clone\n\nWe use the `develop` brand as the release branch, thus `git clone` the repository and `git checkout develop` in order to get the latest version in development.\n\n```\ngit clone git@github.com:FlorentPajot/pandas-aws.git\n```\n\n## Preparing your environment\n\nPandas AWS uses `poetry` to manage dependencies. Thus, `poetry` is required:\n\n`curl -SSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python`\n\nCreate a separate Python environment, for example using `pyenv` along with `pyenv-virtualenv` and Python 3.7.7:\n\n```\npyenv install 3.7.7\npyenv virtualenv 3.7.7 pandas-aws\npyenv activate pandas-aws\n```\n\nCheck your environment using:\n```\nwhich python\n// should show something like .pyenv/shims/python\npython -V\n// should show python 3.7.7 (or any other version you selected)\npip list\n// should show barely nothing except pip and setuptools\n```\n\nIn cas your encounter a problem, check `Pyenv` documentation.\n\nThen install dependencies with poetry after your `git clone` from the project repository:\n\n`poetry install`\n\n## Guidelines\n\nTodo\n\n## Requires\nThe project needs the following dependencies:\n- libpq-dev (psycopg2 dependency)\n",
    'author': 'FlorentPajot',
    'author_email': 'pro.florent.pajot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/FlorentPajot/pandas-aws',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<3.9.0',
}


setup(**setup_kwargs)
