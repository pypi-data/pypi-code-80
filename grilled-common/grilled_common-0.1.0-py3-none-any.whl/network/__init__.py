# -*- encoding: utf-8 -*-
'''
@文件    :network.py
@说明    :
@时间    :2021/01/28 10:32:51
@作者    :hans
@版本    :1.0
'''


from itertools import islice
from networkx import shortest_simple_paths


def k_shortest_paths(G, source, target, k, weight=None):
    
    return list(
        islice(shortest_simple_paths(G, source, target, weight=weight), k)
    )