#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2021/3/18 21:43
# @Author : 詹荣瑞
# @File : setup.py
# @desc : 本代码未经授权禁止商用
from setuptools import setup, find_packages

setup(
    name="BoneTeX",
    version="0.0.1",
    author="六个骨头",
    author_email="2742392377@qq.com",
    description="BoneTeX-GUI是一个基于BoneTeX的高效LaTeX文档编写工具，"
                "通过使用Python脚本自动生产大量繁琐重复的高质量代码，大大提高了编写文档的效率和质量。",
    # 项目主页
    url="https://gitee.com/zrr1999/bonetex",
    # 你要安装的包，通过 setuptools.find_packages 找到当前目录下有哪些包
    packages=find_packages()
)
