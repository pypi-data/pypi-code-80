import pretty_errors
import pandas as pd
from tqdm import tqdm
from tqdm import trange
import numpy as np
import random
import scipy.optimize as sco
import time
import sys
from .picture import scatter
from .picture import pie
from .GetData import StockData
from .GetData import HolidayStockData
import os
sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from ..log.SlyLog import sprint
from ..log.SlyLog import slog


class calculate(object):
    def __init__(self):
        pass

    def correlation(self, x, y):
        if type(x) == list:
            x = np.array(x)
        if type(y) == list:
            y = np.array(y)
        return (np.dot([xi - np.mean(x) for xi in x], [yi - np.mean(y) for yi in y])/(len(x)-1))/((x.std())*(y.std()))

    def weight(self, lists=['A', 'B', 'C'], mode='dict'):
        if mode == 'dict':
            weights = np.random.dirichlet(np.ones(len(lists)), size=1)[0]
            rand = {}
            for i in range(0, len(lists)):
                rand[lists[i]] = weights[i]
            return rand
        elif mode == 'list':
            weights = np.random.dirichlet(np.ones(len(lists)), size=1)[0]
            rand = {}
            for i in range(0, len(lists)):
                rand[lists[i]] = weights[i]
            return list(rand.values())


class Markowit(calculate):
    def __init__(self, names=['贵州茅台', '隆基股份'],
                 start_date='2020-12-01',
                 end_date='2020-12-31',
                 frequency="d",
                 holiday=False,
                 holiday_name=None,
                 before=-21, after=21,
                 no_risk_rate=0.45/5200
                 ):
        '''
        马科维兹投资组合
        '''
        self.sprint = sprint()
        self.slog = slog('Markowit')
        self.no_risk_rate = no_risk_rate
        self.frequency = frequency
        self.names = names
        self.start_date = start_date
        self.end_date = end_date
        self.slog.log(f'time: {self.start_date} ~~ {self.end_date}', mode=1)
        self.slog.log(f'stocks: {self.names}', mode=1)
        self.slog.log(f'frequency: {self.frequency}', mode=1)
        self.slog.log(
            f'risk-free interest rate: {round(self.no_risk_rate,6)}', mode=1)
        try:
            os.makedirs('./picture')
        except:
            pass
        cache = False
        while cache == False:
            try:
                self.stock_data = pd.read_csv(f'cache\\{self.names}.csv')
                self.sprint.cyan('Use cache data to calculate!')
                break
            except:
                self.sprint.cyan('No cache data found!')
                cache = True
                self.sprint.red(
                    'Please make sure that all of the stocks are in the market!')
                self.sprint.green('initializing...')
                if holiday == False:
                    self.StockData = StockData(names=names,
                                               start_date=start_date,
                                               end_date=end_date,
                                               frequency=frequency,
                                               cache=cache)
                    self.codes, self.stock_pair, self.stock_data = self.StockData.stock_data
                    self.StockData.quit()
                else:
                    if holiday_name == None:
                        holiday_name = '国庆节'
                    self.holiday_name = holiday_name
                    start_date = self.start_date.replace('-', '')
                    end_date = self.end_date.replace('-', '')
                    self.HolidayStockData = HolidayStockData(names=names,
                                                             start_date=start_date,
                                                             end_date=end_date,
                                                             holiday=holiday_name,
                                                             frequency=frequency,
                                                             before=before, after=after,
                                                             cache=cache)
                    self.codes, self.stock_pair, self.stock_data = self.HolidayStockData.HolidayNearbyData
                break

    def sharp(self, weights=[], stock_list=[]):
        if weights == []:
            weights = len(self.names) * [1. / len(self.names), ]
        if stock_list == []:
            stock_list = self.names
        df_temp = self.stock_data[['pctChg', 'name']]
        df = df_temp[['name']]
        df['pctChg'] = df_temp['pctChg'].astype('float')
        del df_temp
        covs = []
        for i in range(0, len(stock_list)):
            for j in stock_list[i:]:
                if stock_list[i] != j:
                    covs.append([stock_list[i], j])
        for i in covs:
            x = list(df[df['name'] == i[0]]['pctChg'])
            y = list(df[df['name'] == i[1]]['pctChg'])
            i.append(self.correlation(x, y))
        dic = {}
        rate = 0
        risk = 0
        c = 0
        rand = {}
        for i in stock_list:
            weight = weights[c]
            rand[i] = weight
            data = list(df[df['name'] == i]['pctChg'])
            Mean = np.mean(data)
            Std = np.std(data)
            rate += Mean*weight
            risk += (weight*Std)**2
            dic[i] = weight*Std
            c += 1
        for i in covs:
            risk += 2*i[2]*dic[i[0]]*dic[i[1]]
        sharp = (rate-self.no_risk_rate)/risk
        return {'sharp': sharp, 'rate': rate, 'risk': risk, 'weight': rand}

    def max_sharp(self, weights, *args):
        stock_list = args[0]
        self.slog.log(f'weights: {weights}', mode=1)
        return -self.sharp(weights=weights, stock_list=stock_list)['sharp']

    def portfolio(self, stock_list=[], accurate=True, number=500):
        if stock_list == []:
            stock_list = self.names
        self.sprint.magenta(f'building a portfolio for {stock_list}')
        try:
            os.makedirs('./result')
        except:
            pass
        if accurate == True:
            opts = sco.minimize(fun=self.max_sharp,
                                x0=len(stock_list) * [1. / len(stock_list), ],
                                method='SLSQP',
                                args=(stock_list,),
                                bounds=tuple((0, 1)
                                             for x in range(len(stock_list))),
                                constraints={'type': 'eq',
                                             'fun': lambda x: np.sum(x) - 1}
                                )
            count = 0
            result = {}
            ans = list(opts['x'])
            for i in stock_list:
                result[i] = ans[count]
                count += 1
            pie(dic=result, path='picture\\weights-pie')
            result = [result, -opts['fun']]
            self.slog.log(f'weights:{result[0]}\nsharp:{result[1]}')
            df = pd.DataFrame([result], columns=['weights', 'sharp'])
            df.to_csv('result\\accurate_result.csv',
                      index=False, encoding='utf8')
            return result
        else:
            lists = []
            for i in trange(number):
                weights = self.weight(lists=stock_list, mode='list')
                sharp = self.sharp(
                    weights=weights, stock_list=stock_list)
                lists.append(list(sharp.values()))
            df = pd.DataFrame(
                lists, columns=['sharp', 'rate', 'risk', 'weight'])
            df = df.sort_values('sharp', ascending=False)
            data = []
            for i, j in df.iterrows():
                data.append([j[1], j[2]])
            scatter(data=data, name=[
                    str(self.names)], title='sharp-scatter', path='picture\\sharp-scatter')
            weights = list(df['weight'])[0]
            sharp = list(df['sharp'])[0]
            pie(dic=weights, path='picture\\weights-pie')
            self.slog.log(f'weights:{weights}\nsharp:{sharp}')
            df.to_csv('result\\not_accurate_result.csv',
                      index=False, encoding='utf8')
            return df


if __name__ == '__main__':
    Markowit = Markowit(names=['隆基股份', '五粮液', '贵州茅台'], start_date='2019-12-01',
                        end_date='2020-12-31',
                        frequency='w',
                        holiday=False,
                        )
    print(Markowit.portfolio(accurate=True))
