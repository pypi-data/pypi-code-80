# -*- coding: utf-8 -*-
# @Author: ander
# @Date:   2021-03-29 16:59:00
# @Last Modified by:   ander
# @Last Modified time: 2021-03-30 02:20:11
import setuptools


setuptools.setup(
    name="thonny-ask-makerbean",
    version="0.0.1",
    author="Maker Bi",
    author_email="by@zaowanwu.com",
    description="",
    url="https://makerbean.com",
    packages=setuptools.find_namespace_packages(),
    install_requires=[
        'thonny>=3.2.7',
        'requests~=2.24.0',
        'pyperclip'
    ],
    package_data={
        "thonnycontrib.ask-makerbean": ['res/*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
