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
    'version': '0.1.2',
    'description': 'A Python client for accessing PancakeSwap Lottery smart contract information through Web3.py',
    'long_description': '# PancakeSwap Lottery - Web3 client\n\nA Python client for accessing [PancakeSwap Lottery](https://pancakeswap.finance/lottery) smart contract information through [Web3.py](https://github.com/ethereum/web3.py).\n\n\n## Install\n```\npip install pancakeswap-lottery\n```\n\n## Usage\n```python\nfrom pancakeswap_lottery import Lottery\n\nlottery = Lottery()\n```\n\n<details>\n    <summary><b>Current Lottery queries (realtime)</b></summary>\n\n- [Issue Index](#issue-index)\n- [Total Amount](#total-amount)\n- [Allocation](#allocation)\n- [Total Addresses](#total-addresses)\n- [Drawed](#drawed)\n- [Drawing Phase](#drawing-phase)\n- [Last Timestamp](#last-timestamp)\n</details>\n<details>\n    <summary><b>Past Lottery queries (using issue index)</b></summary>\n\n- [Total rewards](#total-rewards)\n- [History Numbers](#history-numbers)\n- [History Amount](#history-amount)\n- [Matching Reward Amount](#matching-reward-amount)\n</details>\n<details>\n    <summary><b>Past Lottery queries (using tokenid)</b></summary>\n\n- [Lottery Numbers](#lottery-numbers)\n- [Reward View](#reward-view)\n</details>\n<details>\n    <summary><b>Misc.</b></summary>\n\n- [Max Number](#max-number)\n- [Min Price](#min-price)\n- [Cake](#cake)\n- [LotteryNFT](#lotterynft)\n- [Balance Of](#balance-of)\n</details>\n\n---\n### Current Lottery queries (realtime)\n#### Issue Index\nCurrent lottery round\n```python\n>>> lottery.get_issue_index()\n435\n```\n\n#### Total Amount\nTotal pot (CAKE) of current lottery round\n```python\n>>> lottery.get_total_amount()\n34977.25\n```\n\n#### Allocation\nPrize pool allocation (percent)\n```python\n>>> lottery.get_allocation()\n{\'1\': 50, \'2\': 20, \'3\': 10}\n```\n\n#### Total Addresses\n```python\n>>> lottery.get_total_addresses()\n200\n```\n\n#### Drawed\nTrue if currenty lottery round is drawed\n```python\n>>> lottery.get_drawed()\nFalse\n```\n\n#### Drawing Phase\nTrue if currenty lottery round is in drawing phase\n```python\n>>> lottery.get_drawing_phase()\nFalse\n```\n\n#### Last Timestamp\n\n```python\n>>> lottery.get_last_timestamp(epoch=False)\n2021-03-27 11:38:49\n```\n\n### Past Lottery queries (using issue index)\n\n\n#### Total rewards\nTotal pot (CAKE)\n```python\n>>> lottery.get_total_rewards(432)\n51384.125\n```\n\n#### History Numbers\nWinning numbers of lottery round\n```python\n>>> lottery.get_history_numbers(432)\n[2, 13, 7, 3]\n```\n\n#### History Amount\nNumbers of tickets matched\n```python\n>>> lottery.get_history_amount(432)\n{\'4\': 1, \'3\': 34, \'2\': 718}\n```\n\n#### Matching Reward Amount\nNumers of tickets matched a specified number\n```python\n>>> lottery.get_matching_reward_amount(432, 3)\n34\n```\n\n### Past Lottery queries (using tokenid)\n\n#### Lottery Numbers\nLottery numbers for a given ticket\n```python\n>>> lottery.get_lottery_numbers(1328060)\n[11, 5, 14, 6]\n```\n\n#### Reward View\nRewards for a given ticket\n```python\n>>> lottery.get_reward_view(1328060)\n0\n```\n\n\n### Misc.\n\n#### Max Number\n```python\n>>> lottery.get_max_number()\n14\n```\n\n#### Min Price\nPrice for one ticket (CAKE)\n```python\n>>> lottery.get_min_price()\n1\n```\n#### Cake\nCAKE contract address\n```python\n>>> lottery.get_cake()\n0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82\n```\n\n#### LotteryNFT\nPLT-token contract address\n```python\n>>> lottery.get_lotteryNFT()\n0x5e74094Cd416f55179DBd0E45b1a8ED030e396A1\n```\n\n#### Balance Of\nGet total number of tickets bought by a given address\n```python\n>>> lottery.get_balance_of("0xc13456A34305e9265E907F70f76B1BA6E2055c8B")\n2673\n```',
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
