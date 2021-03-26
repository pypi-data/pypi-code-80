# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_pqrnn']

package_data = \
{'': ['*']}

install_requires = \
['bandit>=1.7.0,<2.0.0',
 'bitstring>=3.1.7,<4.0.0',
 'datasets>=1.4.1,<2.0.0',
 'mmh3>=2.5.1,<3.0.0',
 'nltk>=3.5,<4.0',
 'numpy>=1.19.2,<2.0.0',
 'pandas>=1.1.3,<2.0.0',
 'pyhash>=0.9.3,<0.10.0',
 'pytorch-lightning>=0.10.0,<0.11.0',
 'rich>=8.0.0,<9.0.0',
 'scikit-learn>=0.23.2,<0.24.0',
 'torch==1.7.1',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['pytorch-pqrnn = pytorch_pqrnn.__main__:app']}

setup_kwargs = {
    'name': 'pytorch-pqrnn',
    'version': '0.1.0',
    'description': 'Pytorch implementation of pQRNN',
    'long_description': '![banner](./banner.png)\n\n<center>\n<a href="https://github.com/ChenghaoMou/pytorch-pQRNN"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a> <a href="https://github.com/psf/black/blob/master/LICENSE"><img alt="License: MIT" src="https://black.readthedocs.io/en/stable/_static/license.svg"></a>\n</center>\n\n## Environment\n\nNote: Because of recent pytorch change (>=1.7), it is not possible to run a QRNN layer without messing up the environment. See <https://github.com/salesforce/pytorch-qrnn/issues/29> for details.\n\n```bash\npip install -r requirements.txt\n```\n\nIf you want to use a QRNN layer, please follow the instructions [here](https://github.com/salesforce/pytorch-qrnn) to install `python-qrnn` first with  downgraded `torch <= 1.4`. \n\n## Usage\n\n```bash\nUsage: run.py [OPTIONS]\n\nOptions:\n  --task [yelp2|yelp5|toxic]      [default: yelp5]\n  --b INTEGER                     [default: 128]\n  --d INTEGER                     [default: 96]\n  --num_layers INTEGER            [default: 2]\n  --batch_size INTEGER            [default: 512]\n  --dropout FLOAT                 [default: 0.5]\n  --lr FLOAT                      [default: 0.001]\n  --nhead INTEGER                 [default: 4]\n  --rnn_type [LSTM|GRU|QRNN|Transformer]\n                                  [default: GRU]\n  --data_path TEXT\n  --help                          Show this message and exit.\n```\n\nDatasets\n\n-   yelp2(polarity): it will be downloaded w/ datasets(huggingface)\n-   yelp5: [json file](https://www.kaggle.com/luisfredgs/hahnn-for-document-classification?select=yelp_reviews.json) should be downloaded to into `data/`\n-   toxic: [dataset](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge) should be downloaded and unzipped to into `data/`\n\n### Example: Yelp Polarity\n\n    python -W ignore run.py --task yelp2 --b 128 --d 64 --num_layers 4\n\n## Benchmarks(not optimized)\n\n| Model                    | Model Size | Yelp Polarity (error rate) | Yelp-5 (accuracy) | Civil Comments (mean auroc) | Command                                                          |\n| ------------------------ | ---------- | -------------------------- | ----------------- | --------------------------- | ---------------------------------------------------------------- |\n| ~~PQRNN (this repo)~~    | ~~78K~~    | ~~6.3~~                    | ~~70.4~~          | ~~TODO~~                    | `--b 128 --d 64 --num_layers 4 --rnn_type QRNN`                  |\n| PRNN (this repo)         | 90K        | 5.5                        | **70.7**          | 95.57                       | `--b 128 --d 64 --num_layers 1 --rnn_type GRU`                   |\n| PTransformer (this repo) | 617K       | 10.8                       | 68              | 86.5                        | `--b 128 --d 64 --num_layers 1 --rnn_type Transformer --nhead 2` |\n| PRADO<sup>1</sup>        | 175K       |                            | 65.9              |                             |                                                                  |\n| BERT                     | 335M       | **1.81**                   | 70.58             | **98.856**<sup>2</sup>      |                                                                  |\n\n1.  [Paper](https://www.aclweb.org/anthology/D19-1506.pdf)\n2.  Best Kaggle Submission\n\n## Credits\n\n[tensorflow](https://github.com/tensorflow/models/tree/master/research/sequence_projection/prado)\n\nPowered by [pytorch-lightning](https://github.com/PyTorchLightning/pytorch-lightning) and [grid.ai](https://www.grid.ai/)\n',
    'author': 'pytorch-pqrnn',
    'author_email': 'mouchenghao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ChenghaoMou/pytorch-pqrnn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
