# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sister']

package_data = \
{'': ['*']}

install_requires = \
['Janome==0.3.10',
 'fasttext==0.9.2',
 'gensim==3.8.3',
 'mecab-python3==0.996.5',
 'numpy==1.19.0',
 'progressbar>=2.5,<3.0',
 'torch==1.5.1',
 'transformers==2.11.0']

setup_kwargs = {
    'name': 'sister',
    'version': '0.2.2',
    'description': 'SISTER (SImple SenTence EmbeddeR)',
    'long_description': '# sister\nSISTER (**SI**mple **S**en**T**ence **E**mbedde**R**)\n\n\n# Installation\n\n```bash\npip install sister\n```\n\n\n# Basic Usage\n```python\nimport sister\nsentence_embedding = sister.MeanEmbedding(lang="en")\n\nsentence = "I am a dog."\nvector = sentence_embedding(sentence)\n```\n\n\n# Supported languages.\n\n- English\n- Japanese\n- French\n\nIn order to support a new language, please implement `Tokenizer` (inheriting `sister.tokenizers.Tokenizer`) and add fastText\npre-trained url to `word_embedders.get_fasttext()` ([List of model urls](https://github.com/facebookresearch/fastText/blob/master/docs/pretrained-vectors.md)).\n\n\n# Bert models are supported for en, fr, ja (2020-06-29).\nActually Albert for English, CamemBERT for French and BERT for Japanese.  \nTo use BERT, you need to install sister by `pip install \'sister[bert]\'`.\n\n```python\nimport sister\nbert_embedding = sister.BertEmbedding(lang="en")\n\nsentence = "I am a dog."\nvector = bert_embedding(sentence)\n```\n\nYou can also give multiple sentences to it (more efficient).\n\n```python\nimport sister\nbert_embedding = sister.BertEmbedding(lang="en")\n\nsentences = ["I am a dog.", "I want be a cat."]\nvectors = bert_embedding(sentences)\n```\n',
    'author': 'sobamchan',
    'author_email': 'oh.sore.sore.soutarou@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
