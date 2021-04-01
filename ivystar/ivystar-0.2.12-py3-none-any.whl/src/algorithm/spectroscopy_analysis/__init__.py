#!encoding=utf-8

'''
波谱分析，含频率谱，包络谱，功率谱分析，将现有代码封装为一类后，供给web侧调用
输入数据为[(),(),()...()]格式,生成器
输出数据为[(),(),()...()]格式,生成器

'''

import pandas as pd
import numpy as np
from ivystar.src.algorithm.spectroscopy_analysis.Spectrum_analysis import spectrum
from ivystar.src.algorithm.spectroscopy_analysis.Envelope_spectrum import envelope
from ivystar.src.algorithm.spectroscopy_analysis.Power_spectrum_density import power
import pdb
import matplotlib.pylab as plt

class SpectroscopyAnalysis(object):
    '''
    对外接口类
    '''

    def __init__(self):
        pass

    def spectrum(self, x, fs=25600, l=32768):
        '''
        x 待分析数据
        fs 采样频率
        l 采样时间
        '''
        S = spectrum(x,fs,l)
        return S

    def envelope(self, x, fs=25600, l=32768):
        '''
        x 待分析数据
        fs 采样频率
        l 采样时间
        '''
        E = envelope(x,fs,l)
        return E

    def power(self, x, fs=25600, l=32768):
        '''
        x 待分析数据
        fs 采样频率
        l 采样时间
        '''
        P = power(x,fs,l)
        return P


