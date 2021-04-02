#!/usr/bin/env python
import os
from setuptools import setup


REQUIREMENTS = ["matplotlib",
                "numpy"]

setup(name='pwg',
      version=0.1,
      description='Publication Worthy Graphics',
      author='Alex Hagen',
      author_email='alexhagen6@gmail.com',
      url='https://github.com/alexhagen/pwg',
      long_description=open('README.md').read(),
      packages=['pwg'],
      install_requires=REQUIREMENTS,
     )
