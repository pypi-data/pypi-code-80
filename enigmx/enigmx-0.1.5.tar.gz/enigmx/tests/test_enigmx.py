"""
@author: Quantmoon Technologies
webpage: https://www.quantmoon.tech//
"""

from enigmx.classEnigmx import EnigmX
#from enigmx.utils import EquitiesEnigmxUniverse
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier 


instance = EnigmX(bartype = 'VOLUME', 
                  method = 'MDA', 
                  base_path = 'C:/data/',
                  cloud_framework = False
                  ) 

params_for_tuning = {
    'max_leaf_nodes': list(range(2, 20)), 
    'min_samples_split': [2, 3, 4]
    }

instance.get_feature_importance(    
                   model = GradientBoostingClassifier(), 
                   list_stocks = ['ACIW'], 
                   score_constraint = 0.3,
                   server_name="WINDOWS-NI805M6",
                   database="BARS_FEATURES",
                   uid = '',
                   pwd='',
                   driver = "{SQL Server}"
                   )

instance.get_model_tunning(exo_process = True, endo_process = True, 
                           exo_model = DecisionTreeClassifier(),  
                           exo_dic_params = params_for_tuning)
    
instance.get_combinatorial_backtest(trials = 11, partitions = 2)
