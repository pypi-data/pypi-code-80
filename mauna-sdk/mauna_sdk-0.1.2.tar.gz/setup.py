# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mauna_sdk',
 'mauna_sdk.api',
 'mauna_sdk.api.enum',
 'mauna_sdk.api.input',
 'mauna_sdk.schema_config']

package_data = \
{'': ['*'], 'mauna_sdk': ['schema/*']}

install_requires = \
['cryptography>=3.4.6,<4.0.0',
 'gql[all]==3.0.0a5',
 'py-gql-client>=1.0.1,<2.0.0',
 'requests>=2.25.1,<3.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.6,<0.7']}

entry_points = \
{'console_scripts': ['codegen = scripts.codegen:main']}

setup_kwargs = {
    'name': 'mauna-sdk',
    'version': '0.1.2',
    'description': 'Mauna SDK',
    'long_description': '# Mauna SDK\n\n## Installation and usage\n\n### Build\n\n`poetry install`\n\n`poetry run codegen`\n\n`poetry build`\n\n### Install\n\n`pip install mauna_sdk`\n\n### Usage\n\n```python\nfrom mauna_sdk import Mauna\nfrom mauna_sdk.api.parse_ace import parseACE\nfrom mauna_sdk.api.enum.a_c_e_output_type import ACEOutputType\n\n\ndeveloper_id = <int> # Check your profile on the dashboard for this.\napi_key = "<64 letter api key available on your mauna dashboard>"\nclient = Mauna(api_key, developer_id)\nresult = parseACE.execute(client, text="John walks.", format=ACEOutputType.drs)\n\nprint(result)\n```\n\n## API list\n\n### api.parseACE\n\nTakes an ACE text and an output format and produces the parsed ACE according to the format\n\n```python\nfrom mauna_sdk import Mauna\nfrom mauna_sdk.api.parse_ace import parseACE\nfrom mauna_sdk.api.enum.a_c_e_output_type import ACEOutputType\n\n\ndeveloper_id = <int> # Check your profile on the dashboard for this.\napi_key = "<64 letter api key available on your mauna dashboard>"\nclient = Mauna(api_key, developer_id)\nresult = parseACE.execute(client, text="John walks.", format=ACEOutputType.drs)\n# result is parseACE.parseACEData.ACEResult(result="drs([A],[predicate(A,walk,named(\'John\'))-1/2])\\n")\n```\n\n### api.parseContext\n\nTakes a list of turns (`{ content: string }`) and parses them to produce a semantic frames-based context object.\n\n```javascript\napi.parseContext: (turns: [{ content: string }]) => {\n  context {\n    mentions [\n      {\n        evokes,\n        phrase\n      }\n    ]\n  }\n}\n```\n\n### api.paraphraseSentence\n\nTakes an english sentence and produces paraphrased versions of it that retain the semantic meaning of the original.\n\n```javascript\napi.paraphraseSentence: (sentence: string, count: Int = 3) => {\n  paraphrases\n}\n```\n\n### api.predictNextTurn\n\nTakes a list of utterances as history and a list of possible alternatives that can be replied with. Returns the most likely alternative and confidence in that prediction.\n\n```javascript\napi.predictNextTurn: (history: [string], alternatives: [string]) => {\n  nextTurn,\n  confidence\n}\n```\n\n### api.matchIntent\n\nTakes a list of intents (with slots) and a user input. Performs structured information extraction to find the correct intent and fill the corresponding slots.\n\n```javascript\napi.matchIntent: (\n  input: string,\n  intent: [string],\n  threshold: Float = 0.7\n) => {\n  matches [\n    {\n      intent,\n      confidence,\n      slots: [\n        {\n          slot,\n          value,\n          match_type,\n          confidence\n        }\n      ]\n    }\n  ]\n}\n```\n\n### api.measureSimilarity\n\nTakes a target sentence and a list of other sentences to compare with for similarity. Returns an array of pairwise similarity scores.\n\n```javascript\napi.measureSimilarity: (sentence: string, compareWith: [string]) => {\n  result {\n    score,\n    sentencePair\n  }\n}\n```\n\n### api.resolveCoreferences\n\n```javascript\napi.resolveCoreferences: (text: string) => {\n  coref: {\n    detected,\n    resolvedOutput, // Rewritten input with all the coreferences resolved\n    clusters: [\n      {\n        mention, // token(s) detected as a mention of an entity\n        references: [\n          {\n            match,\n            score\n          }\n        ]\n      }\n    ]\n  }\n}\n```\n\n### api.toVec\n\nTakes an English text as an input and returns vector representation for passage, its sentences and entities if found.\n\n```javascript\napi.toVec: (text: string) => {\n  has_vector,\n  vector,\n  vector_norm,\n  sentences: {\n    has_vector,\n    vector_norm,\n    vector,\n    text\n  }\n  entities: {\n    text,\n    has_vector,\n    vector_norm,\n    vector\n  }\n}\n```\n\n### api.getSentiment\n\nTakes plain English input and returns overall and sentence-level sentiment information. Represents positivity or negativity of the passage as a floating point value.\n\n```javascript\napi.getSentiment: (text: string) => {\n  sentiment,\n  sentences: {\n    text,\n    sentiment,\n  }\n}\n```\n\n### api.parseText\n\nTakes some plain English input and returns parsed categories, entities and sentences.\n\n```javascript\napi.parseText: (text: string) => {\n  categories: {\n    label,\n    score\n  },\n  entities: {\n    label,\n    lemma,\n    text\n  },\n  sentences: {\n    text,\n    label,\n    lemma\n  }\n}\n```\n\n### api.extractNumericData\n\nTakes some text and extracts numeric references as a list of tokens with numeric annotations.\n\n```javascript\napi.extractNumericData: (text: string) => {\n  tokens: [\n    {\n      numeric_analysis: {\n        data, // numeric data\n        has_numeric // does this token have numeric info?\n      }\n    }\n  ]\n}\n```\n\n### api.parseTextTokens\n\nTakes some plain English string as input and returns a list of its tokens annotated with linguistic information.\n\n```javascript\napi.parseTextTokens: (text: string) => {\n  tokens: [\n    {\n      dependency, // Type of dependency: PNP, VB ...\n      entity_type, // Type of entity: PERSON ...\n      is_alpha,\n      is_currency,\n      is_digit,\n      is_oov, // is out of vocabulary\n      is_sent_start,\n      is_stop,\n      is_title,\n      lemma,\n      like_email,\n      like_num,\n      like_url,\n      part_of_speech, // verb, noun ...\n      prob,\n      tag,\n      text\n    }\n  ]\n}\n```\n\n### api.renderCSS\n\nTakes ssml and corresponding styles as a css string. Returns base64 encoded audio.\n\n```javascript\napi.renderCSS: (ssml: string, css: string) => {\n  result // base64 encoded audio\n}\n```\n\n### api.speechToText\n\nTakes base64 encoded audio as input and returns a list of possible transcripts (sorted in order of decreasing confidence).\n\n\n```javascript\napi.speechToText: (audio: string) => {\n  transcript: [\n    {\n      text\n    }\n  ]\n}\n```\n\n### api.textToSpeech\n\nTakes text (`string`) as input and returns audio encoded as a base64 string.\n\n```javascript\napi.textToSpeech: (text: string) => {\n  audio // base64 encoded audio\n}\n```\n',
    'author': 'Dmitry Paramonov',
    'author_email': 'asmatic075@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
