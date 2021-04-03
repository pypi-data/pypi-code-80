#!/usr/bin/env python
from io import open
from setuptools import setup, find_packages
files = ["./*"]
setup(
    name='bertforyou',
    version='1.1.0',
    description='a package for your bert using',
    long_description='使用keras实现你的bert项目',
    author='xiaoguzai',
    author_email='474551240@qq.com',
    license='Apache License 2.0',
    url='https://github.com/boss2020/tfbert',
    download_url='https://github.com/boss2020/tfbert/master.zip',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'setuptools',
        'tensorflow>=2.4.0rc0'
    ]
)
