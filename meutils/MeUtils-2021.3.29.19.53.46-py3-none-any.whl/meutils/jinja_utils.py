#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : jinja_utils
# @Time         : 2021/3/26 11:47 上午
# @Author       : yuanjie
# @WeChat       : 313303303
# @Software     : PyCharm
# @Description  : 



from jinja2 import Template, Environment, PackageLoader, FileSystemLoader

# env = Environment(loader=FileSystemLoader('./'))
env = Environment(loader=PackageLoader('meutils'))

# template = env.get_template('demo.j2')