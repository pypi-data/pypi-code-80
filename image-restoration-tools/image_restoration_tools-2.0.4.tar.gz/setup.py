#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys
 
setup(
    name="image_restoration_tools",
    version="2.0.4",
    author="Leo",
    author_email="zxy2019@pku.edu.cn",
    description="a package of image restoration by leo",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/zxy110/image_restoration_tools",
    packages=["image_restoration_tools"],
    include_package_data = True,
    zip_safe = True,
    data_files = ['image_restoration_tools/models/jpeg.pth','image_restoration_tools/models/gaussian_noise.pth','image_restoration_tools/models/gaussian_blur.pth','image_restoration_tools/models/srn/deblur.model.index','image_restoration_tools/models/srn/deblur.model.data-00000-of-00001','image_restoration_tools/models/srn/deblur.model.meta'],
)