#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shlex

from setuptools import setup

depend_packages=[
       'PySide6',
       'matplotlibqml',
]

from distutils.core import setup, Command
import os, sys
import subprocess

class UicCommand(Command):
    description = "custom uic gen command that gen the python code which keep sync with .ui file"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        print(rf'cwd is {os.getcwd()}')
        return subprocess.check_call(shlex.split('uic -g python src/irv/mainwindow.ui -o src/irv/mainwindow.py'))

setup(
    name='irv',
    version='0.00.6',
    description='ISMRMRD rawdata view and analysis tools',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    install_requires=depend_packages,
    author='Cong Zhang',
    author_email='congzhangzh@gmail.com',
    maintainer='Cong Zhang',
    maintainer_email='congzhangzh@gmail.com',
    url='https://github.com/medlab/ismrmrd-rawdata-viewer',
    packages=['irv'],
    package_dir={'':'src'},
    package_data={'':['**/*.ui']},
    # stuff omitted for conciseness.
    cmdclass={
        'uic': UicCommand
    },
    #data_files=['gadm/test_datas/testdata.h5'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)