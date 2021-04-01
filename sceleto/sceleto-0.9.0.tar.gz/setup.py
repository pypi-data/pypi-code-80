from setuptools import setup, find_packages

setup(
#####Needed to silence warnings (and to be a worthwhile package)#####
name='sceleto',
#license='NULL'
#url='NULL'
author='Jongeun Park',
#secondary_author='Sean Lee'
author_email='jp24@kaist.ac.kr',
description='Tool to aid in single cell analysis (temporary description)',
#####Needed to actually package something#####
#packages=['sceleto'],
include_package_data=True,
python_requires='>=3.7',
packages=find_packages(include=['sceleto','sceleto.*','.']),
#####Needed dependencies#####
#package_data={
#    '.git': ['*'],
#    '.ipynb_checkpoints': ['*'],
#    'annotations': ['*','*.csv'],
#    'dandelion' : ['*']
#    'data' : ['*']
#    'examples' : ['*']
#    'matrix' : ['*']
#    'star' : ['*']
#},
install_requires=[
   'pandas',
   'numpy',
   'scanpy>=1.6.1',
   'scipy',
   'seaborn',
   'networkx',
   'python-igraph==0.9.1',
   'bbknn==1.4.1',
   'geosketch',
   'scrublet',
   'joblib',
   'datetime',
   'harmonypy',
   'matplotlib',
   'geosketch',
   'scrublet',
   'adjustText',
   'numba==0.52.0'
],
#####Suggested for Sharing#####
version='0.9.0',
#####Helps with search(?)#####
keywords=['sceleto', 'Scanpy', 'single cell', 'scRNA-seq'],
#####Potential future readme#####
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
zip_safe=False,
)
