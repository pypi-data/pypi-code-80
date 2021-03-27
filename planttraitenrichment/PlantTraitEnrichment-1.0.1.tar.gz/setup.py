# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 13/07/2020 PM 8:23
@Author: xinzhi yao
"""

import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="PlantTraitEnrichment",
  version="1.0.1",
  author="Xinzhi_Yao",
  author_email="xinzhi_bioinfo@163.com",
  description="A python package for plant trait enrichment analysis.",
  long_description=long_description,
  # long_description_content_type="text/markdown",
  long_description_content_type="text/markdown",
  url="https://github.com/YaoXinZhi/Plant-Trait-Enrichment",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)
