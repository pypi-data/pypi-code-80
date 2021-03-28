import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


class Indicator:

    def __init__(self):
        self.model_name = None
        self.model = None
        
        self.data = None
        self.X = None
        self.y = None
        
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None
        
        self.default_features = ['规划期', '入土比', '含钢量']

    # 返回已训练模型的rMSE
    def rmse(self):
        return np.sqrt(mean_squared_error(self.y_test, self.y_pred))

    # 返回已训练模型的MAPE
    def mape(self):
        return np.mean(np.abs((self.y_pred - self.y_test) / self.y_test)) * 100

    # 读取数据
    def read_data(self, file_name):
        self.data = pd.read_csv(file_name)

    # 对已读取的数据进行处理
    def preprocess(self, variable=[]):
        # 数据的预处理
        for var in self.default_features:
            if var in variable:
                variable.remove(var)
        X_default = self.data[self.default_features]
        X_change = self.data[variable]

        self.X = pd.concat([X_default, X_change], axis=1)
        self.y = self.data['经济指标']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=0)

    def fit_model(self, model):

        if model == 'OLS':
            self.__fit_ols()
        elif model == 'DecisionTree':
            self.__fit_decisiontree()
        elif model == 'AdaBoost':
            self.__fit_adaboost()
        elif model == 'GradientBoosting':
            self.__fit_gradientboosting()
        elif model == 'ExtraTree':
            self.__fit_extratree()
        elif model == 'RandomForest':
            self.__fit_randomforest()
        elif model == 'CatBoost':
            self.__fit_catboost()
        elif model == 'LightGBM':
            self.__fit_lightgbm()
        else:
            raise ValueError

        self.model_name = model

    def __fit_ols(self):
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def __fit_decisiontree(self):
        from sklearn.tree import DecisionTreeRegressor
        self.model = DecisionTreeRegressor()
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def __fit_adaboost(self):
        from sklearn.ensemble import AdaBoostRegressor
        self.model = AdaBoostRegressor()
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def __fit_gradientboosting(self):
        from sklearn.ensemble import GradientBoostingRegressor
        self.model = GradientBoostingRegressor()
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def __fit_extratree(self):
        from sklearn.tree import ExtraTreeRegressor
        self.model = ExtraTreeRegressor()
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def __fit_randomforest(self):
        from sklearn.ensemble import RandomForestRegressor
        self.model = RandomForestRegressor()
        self.model.fit(self.X_train, self.y_train)
        self.y_pred = self.model.predict(self.X_test)

    def __fit_catboost(self):
        from catboost import CatBoostRegressor
        # CatBoost中的loss_function的名字
        params = {
            'iterations': 330,
            'learning_rate': 0.1,
            'depth': 10,
            'loss_function': 'RMSE'
        }
        self.model = CatBoostRegressor(**params)
        self.model.fit(self.X_train, self.y_train, plot=True, eval_set=(self.X_test, self.y_test), verbose=3)
        self.y_pred = self.model.predict(self.X_test)

    def __fit_lightgbm(self):
        import lightgbm as lgb

        lgb_params = {
            'boosting_type': 'gbdt',
            'objective': 'regression',
            'metric': {'l2', 'l1'},
            'num_leaves': 31,
            'learning_rate': 0.05,
            'feature_fraction': 0.9,
            'bagging_fraction': 0.8,
            'bagging_freq': 5,
            'verbose': 0
        }
        lgb_train = lgb.Dataset(self.X_train, self.y_train)
        lgb_eval = lgb.Dataset(self.X_test, self.y_test, reference=lgb_train)
        self.model = lgb.train(lgb_params,
                          lgb_train,
                          num_boost_round=20,
                          valid_sets=lgb_eval,
                          early_stopping_rounds=5)
        self.y_pred = self.model.predict(self.X_test, num_iteration=self.model.best_iteration)


"""
    def one_variable_influ(self, one_variable):
        discrete_var = ['适用时间', '所属线路', '规划期', '施工工艺', '连续墙宽度', '车站地质', '混凝土强度']
        continuous_var = ['含钢量', '含砼量', '车站埋深', '入土比']
        X_sample = self.X.loc[[0]]  # 取第一行数据作为控制变量的样本

        if one_variable in discrete_var:
            discrete = one_variable
            if discrete == '适用时间':
                discrete_var_value = ['2010年第一季度', '2018年第三季度', '2009年第三季度', '2007年第一季度',
                                      '2012年第二季度', '2019年第一季度', '2017年第一季度', '2017年第二季度', 
                                      '2015年第二季度', '2020年第二季度', '2012年第三季度', '']
            elif discrete == '所属线路':
                discrete_var_value = ['七号线（首期）', '五号线（东延段）', '十四号线', '二十二号线', 
                                      '六号线（二期）', '十八号线', '广佛线', '十三号线', '二十一号线',
                                      '十三号线（二期）', '十二号线', '十一号线']
            elif discrete == '规划期':
                discrete_var_value = ['十一五', '十二五', '十三五']
            elif discrete == '施工工艺':
                discrete_var_value = ['铁槽机', '双轮铣', '液压抓斗']
            elif discrete == '连续墙宽度':
                discrete_var_value = ['六十', '一百二十', '一百', '八十']
            elif discrete == '车站地质':
                discrete_var_value = ['软土', '灰岩', '花岗岩', '红层']
            elif discrete == '混凝土强度':
                discrete_var_value = ['C20', 'C25', 'C15', 'C30', 'C35']

            # 对variable做规定   注：此时已是编码后的数据
            discrete_data = list(self.X[discrete])
            discrete_value = list(np.unique(discrete_data))  # 记录所有取值并提取中其中不同的取值
            # 初始化列表
            x_change = []
            y_change = []
            # 对每一个取值预测并画图
            for x in discrete_value:
                X_sample.loc[:, discrete] = x
                y_sample = int(self.model.predict(X_sample))
                x_change.append(x)
                y_change.append(y_sample)
            for x in x_change:
                x = str(x)
            plt.bar(discrete_var_value, y_change)
            plt.xticks(rotation=45)
            plt.title(discrete + '取值对经济指标的影响')
            plt.show()

        elif one_variable in continuous_var:
            continuous = one_variable
            # 对continuous做规定
            continuous_data = list(self.data[continuous])
            continuous_value = list(np.unique(continuous_data))
"""


