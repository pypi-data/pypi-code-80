# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 28/03/2021 22:58
@Author: XINZHI YAO
"""

from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name="enrRiceTrait",
  version="1.0.1",
  author="Xinzhi_Yao",
  author_email="xinzhi_bioinfo@163.com",
  description="A python package for Rice Trait Enrichment.",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/YaoXinZhi/enrRiceTrait",
  packages=find_packages('src'),
  package_dir={'': 'src'},
  include_package_data=True,
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)

