"""
Created on Wen Apr 8 10:18 2020

@author: Hanwen Xu

E-mail: hw-xu16@mails.tsinghua.edu.cn

New update: process data with unknown content
"""
from setuptools import setup, find_packages

setup(
    name="seqRegressionModels",
    version="0.0.1",
    keywords=("pip", "seqRegressionModels"),
    description="seqRegression models used by WangLab",
    long_description="Including three models",
    license="Hanwen",

    url="https://github.com/WangLabTHU/RareDecipher/",
    author="Hanwen Xu",
    author_email="xuhw20@mails.tsinghua.edu.cn",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['numpy', 'torch', 'scipy', 'sklearn', 'statsmodels', 'pandas']
)