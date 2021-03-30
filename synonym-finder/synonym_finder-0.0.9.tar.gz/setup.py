from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='synonym_finder',
      version='0.0.9',
      description='This package consists of synonym finder class ',
      url='https://github.com/AlouiAmine/Synonym-Finder',
      author='Aloui Amine',
      author_email='aloui@eurecom.fr',
      license='MIT',
      packages=['synonym_finder'],
      install_requires=['pywikibot', 'SPARQLWrapper', 'nltk', 'sentence_transformers','joblib'],
      python_requires='>=3.5',
      include_package_data=True,
      zip_safe=True)
