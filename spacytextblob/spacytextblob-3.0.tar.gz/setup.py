# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacytextblob']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=3.0,<4.0', 'textblob>=0.15.3,<0.16.0']

setup_kwargs = {
    'name': 'spacytextblob',
    'version': '3.0',
    'description': 'A TextBlob sentiment analysis pipeline compponent for spaCy',
    'long_description': '# spaCyTextBlob\n\nA TextBlob sentiment analysis pipeline compponent for spaCy. \n\nVersion 3.0 is a major version update providing support for spaCy 3.0\'s new interface for adding pipeline components. As a result, it is not backwards compatible with previous versions of spaCyTextBlob. For compatability with spaCy 2.0 please use `pip install spacytextblob==0.1.7`.\n\n*Note that version 1.0, and 2.0 have been skipped. The numbering has been aligned with spaCy\'s version numbering in the hopes of making it easier to compar.*\n\n- [Docs](https://spacytextblob.netlify.app/)\n- [GitHub](https://github.com/SamEdwardes/spaCyTextBlob)\n- [PyPi](https://pypi.org/project/spacytextblob/)\n\n## Table of Contents\n\n- [Install](#install)\n- [Quick Start](#quick-start)\n- [Quick Reference](#quick-reference)\n- [Reference and Attribution](#reference-and-attribution)\n\n## Install\n\nInstall spaCyTextBlob from pypi.\n\n```bash\npip install spacytextblob\n```\n\nTextBlob also requires some data to be downloaded before getting started.\n\n```bash\npython -m textblob.download_corpora\n```\n\nspaCy requires that you download a model to get started.\n\n```bash\npython -m spacy download en_core_web_sm\n```\n\n## Quick Start\n\nspaCyTextBlob allows you to access all of the attributes created by TextBlob sentiment method but within the spaCy framework. The code below will demonstrate how to use spaCyTextBlob on a simple string.\n\n\n```python\ntext = "I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy."\n```\n\nUsing `spaCyTextBlob`:\n\n\n```python\nimport spacy\nfrom spacytextblob.spacytextblob import SpacyTextBlob\n\nnlp = spacy.load(\'en_core_web_sm\')\nnlp.add_pipe("spacytextblob")\ndoc = nlp(text)\n```\n\n\n```python\nprint(\'Polarity:\', doc._.polarity)\n```\n\n    Polarity: -0.125\n    \n\n\n```python\nprint(\'Sujectivity:\', doc._.sentiment.subjectivity)\n```\n\n    Sujectivity: 0.9\n    \n\n\n```python\nprint(\'Assessments:\', doc._.sentiment.assessments)\n```\n\n    Assessments: [([\'really\', \'horrible\'], -1.0, 1.0, None), ([\'worst\', \'!\'], -1.0, 1.0, None), ([\'really\', \'good\'], 0.7, 0.6000000000000001, None), ([\'happy\'], 0.8, 1.0, None)]\n    \n\nUsing `TextBlob`:\n\n\n```python\nfrom textblob import TextBlob\nblob = TextBlob(text)\n```\n\n\n```python\nprint(blob.sentiment_assessments.polarity)\n```\n\n    -0.125\n\n\n\n```python\nprint(blob.sentiment_assessments.subjectivity)\n```\n\n    0.9\n\n\n\n```python\nprint(blob.sentiment_assessments.assessments)\n```\n\n    [([\'really\', \'horrible\'], -1.0, 1.0, None), ([\'worst\', \'!\'], -1.0, 1.0, None), ([\'really\', \'good\'], 0.7, 0.6000000000000001, None), ([\'happy\'], 0.8, 1.0, None)]\n\n\n## Quick Reference\n\nspaCyTextBlob performs sentiment analysis using the [TextBlob](https://textblob.readthedocs.io/en/dev/quickstart.html) library. Adding spaCyTextBlob to a spaCy nlp pipeline provides access to three new extension attributes.\n\n- `._.polarity`\n- `._.subjectivity`\n- `._.assessments`\n\nThese extension attributes can be accessed at the `Doc`, `Span`, or `Token` level.\n\nPolarity is a float within the range [-1.0, 1.0], subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective, and assessments is a list of polarity and subjectivity scores for the assessed tokens.\n\n## Reference and Attribution\n\n- TextBlob\n    - [https://github.com/sloria/TextBlob](https://github.com/sloria/TextBlob)\n    - [https://textblob.readthedocs.io/en/latest/](https://textblob.readthedocs.io/en/latest/)\n- negspaCy (for inpiration in writing pipeline and organizing repo)\n    - [https://github.com/jenojp/negspacy](https://github.com/jenojp/negspacy)\n- spaCy custom components\n    - [https://spacy.io/usage/processing-pipelines#custom-components](https://spacy.io/usage/processing-pipelines#custom-components)\n',
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SamEdwardes/spaCyTextBlob',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
