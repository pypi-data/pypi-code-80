# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 14:56:44 2021

@author: HanaFI
"""

from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My first Strategy package'
LONG_DESCRIPTION = "".join("My first package which should help systematize"+
                           "the back-end of strategy trading, from underlying"+
                           "selection portfolio optimization.")

# Setting up
setup(
        name="StratBox",
        version=VERSION,
        author="Kelian Ferhat",
        author_email="<kelianferhat@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that
        # needs to be installed along with your package.

        keywords=['python', 'finance'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
