import os
import re
import sys
import platform
from subprocess import CalledProcessError 
import setuptools 
from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
import io
with io.open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


__version__ = '0.1.0'

kwargs = dict(
    name='fullresattn',
    version=__version__,
    author='Lianfa Li',
    author_email='lspatial@gmail.com',
    description='Library for full residual deep network with attention layers',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    zip_safe=False, 
    install_requires = [],
    packages=find_packages(), 
    include_package_data=True,
    classifiers=[
        'Development Status :: 6 - Mature',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    data_files=[('csv', ['fullresattn/data/pm25selsample.csv', 'fullresattn/data/simdata.csv'])],
)

# likely there are more exceptions, take a look at yarl example 
try: 
    setup(**kwargs)   
except CalledProcessError: 
    print('Failed to build extension!') 
    del kwargs['ext_modules'] 
    setup(**kwargs) 

