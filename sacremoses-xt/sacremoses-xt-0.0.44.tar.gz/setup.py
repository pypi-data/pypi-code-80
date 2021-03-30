from distutils.core import setup
import setuptools

console_scripts = """
[console_scripts]
sacremoses=sacremoses.cli:cli
"""

setup(
  name = 'sacremoses-xt',
  packages = ['sacremoses'],
  version = '0.0.44',
  description = 'SacreMoses (Extended)',
  long_description = 'MosesTokenizer in Python',
  author = '',
  package_data={'sacremoses': ['data/perluniprops/*.txt', 'data/nonbreaking_prefixes/nonbreaking_prefix.*']},
  url = 'https://github.com/isi-nlp/sacremoses',
  keywords = [],
  classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  install_requires = ['regex', 'six', 'click', 'joblib', 'tqdm'],
  entry_points=console_scripts,
)
