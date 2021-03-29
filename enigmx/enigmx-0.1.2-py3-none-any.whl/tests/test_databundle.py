"""
@author: Quantmoon Technologies
webpage: https://www.quantmoon.tech//
"""

from enigmx.utils import EquitiesEnigmxUniverse
from enigmx.databundle_interface import SQLEnigmXinterface

server_name = "DESKTOP-N8JUB39"
pathzarr = 'D:/data_repository/'
list_stocks = EquitiesEnigmxUniverse[10:20]
start_date = "2020-08-09" 
end_date = "2020-09-09" 
desired_bars = 10
bartype = 'volume'

print("inicializando clase")
enigmxsql = SQLEnigmXinterface(
    server = server_name, 
    pathzarr = pathzarr, 
    list_stocks = list_stocks, 
    bartype = bartype, 
    start_date = start_date, 
    end_date = end_date, 
    desired_bars = desired_bars)

print("creando tablas")
enigmxsql.create_table_database(
    bars_tunning = False, 
    bars_basic = False, 
    bars_entropy = False, 
    etfs_trick = False, 
    bars_sampled = False, 
    bars_barrier = False,
    bars_weights = False,
    bars_features = False,
    creation_database = False)

print("subiendo info")
enigmxsql.compute_info_to_sql(
    bars_tunning_process = False, 
    bar_construction_process = False, 
    entropy_construction_process = False, 
    etftrick_construction_process = False, 
    sampling_features_process = False, 
    triple_barrier_computation_process = False,
    sample_weight_computation_process = False,
    features_bar_computation_process = False,
    )

