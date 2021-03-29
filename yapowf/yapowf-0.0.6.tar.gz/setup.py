from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()
    
 
classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
  'Programming Language :: Python :: 3',
]
 
setup(
  name='yapowf',
  version='0.0.6',
  description='A new Python Power Factory API',
  long_description=long_description,
  url='',  
  author='Camilo Romero',
  author_email='camilo.romers@gmail.com',
  license='GNU GPLv3', 
  classifiers=classifiers,
  keywords=['power factory api', 'digsilent python'], 
  packages=find_packages(),
  install_requires=['pandas'] 
)