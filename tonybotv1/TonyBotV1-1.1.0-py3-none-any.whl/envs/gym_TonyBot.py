import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt
import math
from pyts.image import GramianAngularField

#gasf = GramianAngularField(image_size=self.image_size, method='summation') : image_size <= window_size


class Actions(Enum):
    Sell = 2
    Buy = 1
    DoNothing = 0


class TradingEnv(gym.Env):
    metadata = {'render.modes': ['human']}    

    def __init__(self, df1, df15, window_size, max_loss, max_profit, stoploss, takeprofit, slipping, image_size, image_count, frame_bound):
        self.seed()
        self.frame_bound = frame_bound
        self.df1 = df1
        self.df15 = df15
        self.window_size = window_size
        self.max_loss = max_loss
        self.max_profit = max_profit
        self.stoploss = stoploss
        self.takeprofit = takeprofit
        self.slipping = slipping
        self.image_size = image_size
        self.prices, self.high, self.low, self.signal_data1h, self.signal_data15 = self._process_data()
        self.shape = (image_count, image_size, image_size)
        self.action_space = spaces.Discrete(len(Actions))
        self.observation_space = spaces.Box(low=-1, high=1, shape=self.shape, dtype=np.float32)
        self._start_tick = self.window_size
        self._end_tick = len(self.prices) -1
        self._done = None
        self._current_tick = None
        #self._last_trade_tick = None
        #self._position = None
        #self._position_history = None
        self._total_reward = None
        self._total_profit = None
        self._first_rendering = None 
        self.history = None
        self.traded = None
        self.traded_list = []

    def seed(self, seed= None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]          


    def reset(self):
        self._done = False
        self.traded = False
        self._current_tick = self._start_tick
        #self._last_trade_tick = None 
        self._total_reward = 0
        self._total_profit = 1
        self._first_rendering = True
        self.history = {}
        self.traded_list = []
        return self._get_observation()


    def step(self, action):
        self._done = False
        self._current_tick += 1
        if self._total_profit <= self.max_loss:
            self._done = True
        if self._current_tick == self._end_tick:
            self._done = True
        if self._total_profit >= self.max_profit:
            self._done = True
        self.traded, step_reward = self._calculate_reward(action)
        self._total_reward += step_reward
        observation = self._get_observation()
        info = dict(
            total_reward = self._total_reward,
            total_profit = self._total_profit
            )
        return observation, step_reward, self._done, info



    def _get_observation(self):
        gasf = GramianAngularField(image_size=self.image_size, method='summation')
        data15_signal = self.signal_data15[(self._current_tick - self.window_size):self._current_tick]
        data15_transpose = np.transpose(data15_signal)
        gasf15 = gasf.fit_transform(data15_transpose)
        time1h = (self._current_tick - self.window_size) / 4
        time1h = math.floor(time1h)
        data1h_signal = self.signal_data1h[time1h:(self.window_size + time1h)]
        data1h_transpose = np.transpose(data1h_signal)
        gasf1h = gasf.fit_transform(data1h_transpose)
        output_data = np.concatenate((gasf1h, gasf15), axis=0)
        return output_data
       

    def _calculate_reward(self, action):
        step_reward = 0
        traded = False
        if action >0 and len(self.traded_list) >0:
            step_reward += -len(self.traded_list)*0.5
        if action ==0 and len(self.traded_list) ==0:
            step_reward += -0.1
        if action ==1 :
            traded_price = self.prices[self._current_tick - 2] + self.slipping
            profit_price = traded_price + self.takeprofit + self.slipping
            stop_price = traded_price - self.stoploss + self.slipping
            self.traded_list.append(np.array([traded_price, profit_price, stop_price, action]))
        if action ==2:
            traded_price = self.prices[self._current_tick -2] - self.slipping
            profit_price = traded_price - self.takeprofit - self.slipping
            stop_price = traded_price + self.takeprofit - self.slipping
            self.traded_list.append(np.array([traded_price, profit_price, stop_price, action]))

        if len(self.traded_list) >0:
            index = np.arange(len(self.traded_list))
            drop_index = []
            for i, j in zip(index, self.traded_list):
                if j[3] ==1:
                    if j[2] >= self.low[self._current_tick-1]:
                        step_reward += -2
                        self._total_profit += -0.02
                        drop_index.append(i)
                    if j[1] <= self.high[self._current_tick-1] and j[2] < self.low[self._current_tick-1]:
                        step_reward += 2
                        self._total_profit += 0.03
                        drop_index.append(i)
                if j[3] ==2:
                    if j[2] <= self.high[self._current_tick-1]:
                        step_reward += -2
                        self._total_profit += -0.02
                        drop_index.append(i)
                    if j[1] >= self.low[self._current_tick-1] and j[2] > self.high[self._current_tick-1]:
                        step_reward += 2
                        self._total_profit += 0.03
                        drop_index.append(i)
            for ele in sorted(drop_index, reverse= True):
                del self.traded_list[ele]
            if len(self.traded_list) >0:
                traded = True
        
        return traded, step_reward

        

    def _process_data(self):
        close15 = self.df15.loc[:, 'Close'].to_numpy() 
        close15 = close15[self.frame_bound[0] - self.window_size:self.frame_bound[1]]
        high15 = self.df15.loc[:, 'High'].to_numpy()
        high15 = high15[self.frame_bound[0] - self.window_size:self.frame_bound[1]]
        low15 = self.df15.loc[:, 'Low'].to_numpy()
        low15 = low15[self.frame_bound[0] - self.window_size:self.frame_bound[1]]
        diff15 = np.insert(np.diff(close15), 0, 0)
        signal_data15 = self.df15.to_numpy()
        signal_data1h = self.df1.to_numpy()

        return close15, high15, low15, signal_data1h, signal_data15


