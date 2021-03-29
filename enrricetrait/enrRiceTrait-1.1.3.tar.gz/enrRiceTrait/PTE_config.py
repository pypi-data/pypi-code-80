# -*- coding:utf-8 -*-
# ! usr/bin/env python3
"""
Created on 14/07/2020 下午11:48
@Author: xinzhi yao
"""

import inspect, os


def get_script_path():
    script_file = inspect.getfile(inspect.currentframe())
    return os.path.abspath(os.path.dirname(script_file))

script_path = get_script_path()
print(script_path)

db_config = {
    'db_path': 'data',
    'ontology_file': f'{script_path}/to.wto.ro.funRiceGene.obo',
    'ontology_url': 'https://raw.githubusercontent.com/YaoXinZhi/Plant-Trait-Enrichment/master/data/to-basic.obo',
    'PT_anno_file': f'{script_path}/Total_Association.txt',
    'PT_anno_url': 'https://raw.githubusercontent.com/YaoXinZhi/Plant-Trait-Enrichment/master/data/Oryzasebase.txt',

}

print(db_config['ontology_file'])
print(db_config['PT_anno_file'])
