from codecs import open
import os
from setuptools import setup, find_packages
#import pypandoc

with open('README.md') as readme_file:
    README = readme_file.read()

VERSION = '0.0.1'
DESCRIPTION = 'FPL Analytics'
#LONG_DESCRIPTION = DESCRIPTION
URL = 'https://github.com/abhijith-git/pyfpl'

# Setting up
setup(
    name="pyfpl",
    version=VERSION,
    author="Abhijith Chandradas",
    author_email="<abhijith.chandradas@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=README,
    url=URL,
    license='MIT',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=['matplotlib', 
                      'pandas', 
                      'numpy',
                      'seaborn'],
    keywords=['python', 
              'football',
              'fpl',  
              'data visualization', 
              'analytics'],
    classifiers=[
            "Development Status :: 1 - Planning",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Topic :: Scientific/Engineering :: Visualization",
            'Topic :: Scientific/Engineering :: Information Analysis',
            "Programming Language :: Python :: 3"]
)

#Display README.md in PYPI
#https://stackoverflow.com/questions/26737222/how-to-make-pypi-description-markdown-work

