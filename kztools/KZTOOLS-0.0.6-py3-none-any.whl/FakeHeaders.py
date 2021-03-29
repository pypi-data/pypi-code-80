# coding: utf-8
# Author：KZ
# Date ：2021/3/29 15:43
# uploadTools
# Tool ：PyCharm
from .FakeUseragent import UserAgent



class Headers():
    def __init__(self):
        self.random =  {"User-Agent": UserAgent().random()}


if __name__ == '__main__':
    headers=Headers().random
    print(headers)