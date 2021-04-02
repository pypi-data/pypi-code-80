# /package/__init__.py
""" Description for Package """

from package.module import Example_class, method
# from package import * 로 써도 된다.

__all__ = ['module']

# 패키지 버전 정의
__version__ = '0.0.1'