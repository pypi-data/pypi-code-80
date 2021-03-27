# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pancakeswap_lottery']

package_data = \
{'': ['*'], 'pancakeswap_lottery': ['assets/*']}

install_requires = \
['web3>=5.17.0,<6.0.0']

setup_kwargs = {
    'name': 'pancakeswap-lottery',
    'version': '0.1.0',
    'description': 'A Python client for accessing PancakeSwap Lottery smart contract information through Web3.py',
    'long_description': '# PancakeSwap Lottery - Web3 client\n\nA Python client for accessing [PancakeSwap Lottery](https://pancakeswap.finance/lottery) smart contract information through Web3.py.\n\n## Documentation\n```python\nfrom pancakeswap_lottery import Lottery\n\nlottery = Lottery()\n```\n\n### Current lottery\n#### get_issue_index\n```python\n>>> lottery.get_issue_index()\n435\n```\n\n#### get_total_amount (Prize pool)\n```python\n>>> lottery.get_total_amount()\n34977.25\n```\n\n#### get_allocation (Prize pool allocation)\n```python\n>>> lottery.get_allocation()\n{\'1\': 50, \'2\': 20, \'3\': 10}\n```\n\n#### get_total_addresses\n```python\n>>> lottery.get_total_addresses()\n200\n```\n\n#### get_drawed\n```python\n>>> lottery.get_drawed()\nFalse\n```\n\n#### get_drawing_phase\n```python\n>>> lottery.get_drawing_phase()\nFalse\n```\n\n#### get_last_timestamp\n```python\n>>> lottery.get_last_timestamp(epoch=False)\n2021-03-27 11:38:49\n```\n\n### Past lotteries (with issue index)\n\n#### get_total_rewards (Prize pool)\n```python\n>>> lottery.get_total_rewards(432)\n51384.125\n```\n\n#### get_history_numbers\n```python\n>>> lottery.get_history_numbers(432)\n[2, 13, 7, 3]\n```\n\n#### get_history_amount (Numers of tickets matched)\n```python\n>>> lottery.get_history_amount(432)\n{\'4\': 1, \'3\': 34, \'2\': 718}\n```\n\n#### get_matching_reward_amount\n```python\n>>> lottery.get_matching_reward_amount(432, 3)\n34\n```\n\n### Past lotteries (with tokenid)\n#### get_lottery_numbers\n```python\n>>> lottery.get_lottery_numbers(1328060)\n[11, 5, 14, 6]\n```\n\n#### get_reward_view\n```python\n>>> lottery.get_reward_view(1328060)\n0\n```\n\n### Lottery metadata\n#### get_max_number\n```python\n>>> lottery.get_max_number()\n14\n```\n\n#### get_min_price\n```python\n>>> lottery.get_min_price()\n1\n```\n\n### Other\n#### get_cake (CAKE contract address)\n```python\n>>> lottery.get_cake()\n0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82\n```\n\n#### get_lotteryNFT (PLT-token contract address)\n```python\n>>> lottery.get_lotteryNFT()\n0x5e74094Cd416f55179DBd0E45b1a8ED030e396A1\n```\n\n#### get_balance_of(address)\n```python\n>>> lottery.get_balance_of("0xc13456A34305e9265E907F70f76B1BA6E2055c8B")\n2673\n```',
    'author': 'Fredrik Haarstad',
    'author_email': 'codemonkey@zomg.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/frefrik/pancakeswap-lottery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
