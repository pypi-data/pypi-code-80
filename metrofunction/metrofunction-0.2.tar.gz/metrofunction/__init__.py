# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt
from sklearn import metrics
import shap
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

'''读入数据'''
#data = pd.read_csv('CZT.csv')

####3.1决策树回归####
from sklearn import tree
model_DecisionTreeRegressor = tree.DecisionTreeRegressor()
####3.2线性回归####
from sklearn import linear_model
####线性回归带参数####
from statsmodels.formula.api import ols
model_LinearRegression = linear_model.LinearRegression()
####3.5随机森林回归####
from sklearn import ensemble
model_RandomForestRegressor = ensemble.RandomForestRegressor(n_estimators=20)#这里使用20个决策树
####3.6Adaboost回归####
from sklearn import ensemble
model_AdaBoostRegressor = ensemble.AdaBoostRegressor(n_estimators=50)#这里使用50个决策树
####3.7GBRT回归####
from sklearn import ensemble
model_GradientBoostingRegressor = ensemble.GradientBoostingRegressor(n_estimators=100)#这里使用100个决策树
####3.9ExtraTree极端随机树回归####
from sklearn.tree import ExtraTreeRegressor
model_ExtraTreeRegressor = ExtraTreeRegressor()
####CatBoost####
from catboost import CatBoostRegressor, Pool
params = {
    'iterations': 330,
    'learning_rate': 0.1,
    'depth': 10,
    'loss_function': 'RMSE'
}
model_CatBoostRegeressor = CatBoostRegressor(**params)
####LightGBM####
#lightgbm需要是2.2.0版本
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
#这两行其实对函数的实际使用没有影响，因为模型的训练是包含在函数里面的
#这一句没有实际意义
model_lgb = []


def AutoFunction(data, type='ols', model=ols, variable=[]):
    #数据处理
    default = ['规划期', '入土比', '含钢量']
    for var in default:
        if var in variable:
            variable.remove(var)
    x_default = data[default]
    x_change = data[variable]
    from pandas import concat
    x = concat([x_default, x_change], join='inner', axis=1)
    y = data['经济指标']
    from sklearn.model_selection import train_test_split
    X_train, X_test, Y_train, Y_test = train_test_split(x, y, train_size=0.8,random_state=0)

    '''线性回归'''
    if type == 'ols':
        y_x = concat([y, x], join='inner', axis=1)
        ols_train, ols_test = train_test_split(y_x, test_size=0.2, random_state=1234)
        formula_str = '经济指标~'
        x_list = x.columns.tolist()
        for x in x_list:
            formula_str = formula_str + x + '+'
        formula_str = formula_str[:-1]
        print(formula_str)
        model = ols(formula=formula_str, data=ols_train).fit()
        print(model.params)
        print(model.summary())
        #不太清楚用stat的ols怎么predict
        model_2 = model_LinearRegression
        model_2.fit(X_train, Y_train)
        Y_pred = model_2.predict(X_test)
        RMSE = sqrt(metrics.mean_squared_error(Y_test, Y_pred))
        print('RMSE:', RMSE)

    '''树模型'''
    Model_Tree = ['model_DecisionTreeRegressor', 'model_AdaBoostRegressor', 'model_GradientBoostingRegressor', 'model_ExtraTreeRegressor', 'model_RandomForestRegressor']
    if type in Model_Tree:
        model.fit(X_train, Y_train)
        Y_pred = model.predict(X_test)
        # 计算RMSE
        RMSE = sqrt(metrics.mean_squared_error(Y_test, Y_pred))
        print('RMSE:', RMSE)
        #绘制变量重要性图
        fea_imp = model.feature_importances_
        fea_imp = 100.0 * (fea_imp / max(fea_imp))
        Tree_Feature_importance = pd.DataFrame({
            'feature': x.columns.tolist(),
            'importance': fea_imp,
        }).sort_values(by='importance', ascending=False)
        Tree_Feature_importance = Tree_Feature_importance.reset_index()
        fig, ax = plt.subplots(figsize=(10, 5), dpi=80)
        ax.vlines(x=Tree_Feature_importance.index, ymin=0, ymax=Tree_Feature_importance.importance, color='firebrick', alpha=0.7,
                  linewidth=2)
        ax.scatter(x=Tree_Feature_importance.index, y=Tree_Feature_importance.importance, s=75, color='firebrick', alpha=0.7)
        ax.set_title('Feature Importance', fontdict={'size': 22})
        ax.set_xticks(Tree_Feature_importance.index)
        ax.set_xticklabels(Tree_Feature_importance.feature, rotation=60,
                           fontdict={'horizontalalignment': 'right', 'size': 12})
        # Annotate
        for row in Tree_Feature_importance.itertuples():
            ax.text(row.Index, row.importance, s=round(row.importance), horizontalalignment='center',
                    verticalalignment='bottom', fontsize=14)
        plt.show()

    '''CatBoost'''
    if type == 'model_CatBoostRegeressor':
        model = model.fit(X_train, Y_train, plot=True, eval_set=(X_test, Y_test),verbose=3)
        Y_pred = model.predict(X_test)
        # 计算RMSE
        RMSE = sqrt(metrics.mean_squared_error(Y_test, Y_pred))
        print('RMSE:', RMSE)
        #特征重要性
        shap_values = model.get_feature_importance(Pool(X_train, Y_train), type='ShapValues')
        shap_values = shap_values[:, :-1]
        shap.summary_plot(shap_values, X_train,max_display=20)
    '''LightGBM'''
    if type == 'LightGBM':
        lgb_train = lgb.Dataset(X_train, Y_train)
        lgb_eval = lgb.Dataset(X_test, Y_test, reference=lgb_train)
        model = lgb.train(lgb_params,
                lgb_train,
                num_boost_round=20,
                valid_sets=lgb_eval,
                early_stopping_rounds=5)
        Y_pred = model.predict(X_test, num_iteration=model.best_iteration)
        # 计算RMSE
        RMSE = sqrt(metrics.mean_squared_error(Y_test, Y_pred))
        print('RMSE:', RMSE)
        lgb_importance = pd.DataFrame({
            'feature': x.columns.tolist(),
            'importance': model.feature_importance(),
        }).sort_values(by='importance', ascending=False)
        lgb_importance = lgb_importance.reset_index()
        fig, ax = plt.subplots(figsize=(10, 5), dpi=80)
        ax.vlines(x=lgb_importance.index, ymin=0, ymax=lgb_importance.importance, color='firebrick', alpha=0.7,
                  linewidth=2)
        ax.scatter(x=lgb_importance.index, y=lgb_importance.importance, s=75, color='firebrick', alpha=0.7)
        # Title, Label, Ticks and Ylim
        ax.set_title('Feature Importance', fontdict={'size': 22})
        ax.set_xticks(lgb_importance.index)
        ax.set_xticklabels(lgb_importance.feature, rotation=60,
                           fontdict={'horizontalalignment': 'right', 'size': 12})
        # Annotate
        for row in lgb_importance.itertuples():
            ax.text(row.Index, row.importance, s=round(row.importance), horizontalalignment='center',
                    verticalalignment='bottom', fontsize=14)
        plt.show()
'''
print('测试一')
AutoFunction()
print('测试二')
AutoFunction('model_RandomForestRegressor', model_RandomForestRegressor, ['含钢量', '施工工艺', '含砼量', '车站埋深', '入土比'])
print('测试三')
AutoFunction('model_CatBoostRegeressor', model_CatBoostRegeressor, ['含钢量', '含砼量', '入土比', '适用时间', '所属线路', '规划期'])
print('测试四')
AutoFunction('LightGBM', model_lgb, ['含钢量', '施工工艺'])
print('测试五')
AutoFunction('model_CatBoostRegeressor', model_CatBoostRegeressor, ['含钢量', '施工工艺', '含砼量', '车站埋深', '入土比', '连续墙宽度', '车站地质', '混凝土强度等级'])
'''