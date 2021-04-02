# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stock_utilities']

package_data = \
{'': ['*']}

install_requires = \
['praw>=7.2.0,<8.0.0',
 'py_vollib>=1.0.1,<2.0.0',
 'scipy>=1.6.1,<2.0.0',
 'yfinance>=0.1.55,<0.2.0']

setup_kwargs = {
    'name': 'stock-utilities',
    'version': '0.1.8',
    'description': 'This library is a wrapper around the finance libraries in order to give out a data model different from raw pandas and be usable in production services',
    'long_description': '# stock_utilities\n\nThis repo will manage utilities for stock data and stock option\nThe idea is to fetch data from multiple sources and use them from a single point and have a library that is typesafe\n\n\nThe used provider are:\n  - YFinance\n\n## Example\n\n```\nimport datetime\nimport praw\nimport stock_utilities\n\ndata = stock_utilities.stock_data.StockData(\n    "GME", stock_utilities.proxy.YFinanceProvider\n)\nprint(data.get_last_price())\ndata = stock_utilities.stock_data.StockData(\n    "GME", stock_utilities.proxy.YFinanceProvider\n)\nhistory = data.get_stock_price_history(\n    interval=datetime.timedelta(days=1), period=datetime.timedelta(days=5)\n)\nassert len(history), 5\n\nhistory_option = data.get_next_friday_option_chain()\nprint(history_option.calls[-1])\nprint(\n    history_option.calls[-1].delta(),\n    history_option.calls[-1].gamma(),\n    history_option.calls[-1].vega(),\n)\n\n\ncombined_providers = stock_utilities.proxy.combine_providers(\n    [stock_utilities.proxy.YFinanceProvider, stock_utilities.proxy.RedditFetcher]\n)\n\nreddit = praw.Reddit(\n   client_id="XXX",\n   client_secret="XXX",\n   user_agent="XXX",\n)\nnew_client = stock_utilities.stock_data.StockData(\n   "GME", combined_providers, reddit_client=reddit\n)\n\nprint(new_client.get_reddit_threads(["wallstreetbets"]))\n```',
    'author': 'Diego Luca Candido',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joxer/stock_utilities',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
