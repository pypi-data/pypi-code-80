#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='GNNs',
    version='0.0.1',
    description=(
        'GNNs is a library for building Graph Neural Network with Python, and this library was writen by Wei Wei.'
    ),
    long_description=open('README.rst').read(),
    author='Wei Wei',
    author_email='w.w@taoxiang.org',
    maintainer='Wei Wei',
    maintainer_email='w.w@taoxiang.org',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='http://www.taoxiang.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[],
)

