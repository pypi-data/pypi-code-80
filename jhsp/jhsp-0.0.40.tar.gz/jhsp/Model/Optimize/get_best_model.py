import os
import sys

# 添加包的顶层目录
top_path = os.path.abspath(__file__)
top_path = top_path.split('jhsp')[0]
top_path = os.path.join(top_path, 'jhsp')
sys.path.append(top_path)


from sklearn.model_selection import RandomizedSearchCV
from jhsp.Model.Optimize import config
from kerastuner.tuners import RandomSearch

class GetBestModel():

    def __init__(self):
        pass

    def GetBestTradition(self,model,parameters,x,y):
        """
        :param model_name:
        :param x:
        :param y:
        :return:
        """

        random_search = RandomizedSearchCV(model,
                                           param_distributions=parameters,
                                           n_iter=config.random_search_n_iter,
                                           cv=config.cross_val_num,
                                           scoring=config.scoring,
                                           random_state=config.random_num,
                                           n_jobs= config.random_search_n_jobs
                                           )

        random_search.fit(x, y)

        best_params = random_search.cv_results_['params'][random_search.best_index_]
        best_model = random_search.best_estimator_

        return best_model,best_params


    def GetBestNNet(self,model_fun,x,y,**kwargs):
        """
        超参数列表已经在构建模型的时候内置到模型里面了，所以不用传入，这人是用keras-tuner调参的一个特性，
        也是与传统调参方法不同的地方。
        """

        tuner = RandomSearch(
            model_fun,
            objective=config.scoring,  # 优化目标
            max_trials=config.max_trials,
            executions_per_trial=config.executions_per_trial,
            directory= model_fun.__name__ +'_dir',
            project_name= model_fun.__name__ ,
        )

        print(tuner.search_space_summary())

        tuner.search(x, y,
                     epochs=config.epochs_num,
                     )

        print(tuner.search_space_summary())
        print(tuner.results_summary())


        return tuner.get_best_models(num_models=1), tuner.results_summary(num_trials=1)













