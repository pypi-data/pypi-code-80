# 功率谱分析
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb

def power(x,Fs,L):
    T = 1/Fs                    # 采样时间
    t = np.arange(L)/Fs         # 时间向量

    y = x-np.mean(x)            #零均值化
    # 画出信号时域图像
    #fig = plt.figure()
    #fig.tight_layout()#调整整体空白
    #plt.subplots_adjust(wspace =0, hspace =.5)#调整子图间距
    #f = fig.add_subplot()
    #f.plot(t,y)
    #f.set_ylim(-25,25)
    #f.set_xlabel('time (seconds)')
    #fig.show()

    # 傅里叶变换
    N = L
    # np.fft.fft，对输入信号进行快速傅里叶变换,输出长度与输入相同
    xdft = np.fft.fft(y,axis=0)
    xdft = xdft[range(int(L/2)+1)]   # 单边频谱,由于对称性，只取一半区间
    psdx = 2 * abs(xdft) ** 2/N      # 求功率谱
    f = Fs/2*np.linspace(0, 1, N//2+1)   # 横坐标，频率

    #绘图显示结果
    #fig1 = plt.figure()
    #fig.tight_layout()#调整整体空白
    #plt.subplots_adjust(wspace =0, hspace =.5)#调整子图间距
    #f1 = fig1.add_subplot(211)
    #f1.plot(f,psdx)
    #f1.set_xlabel('Frequency (Hz)')
    #f1.set_title('Single-Sided Amplitude Spectrum of y(t)')
    #f2 = fig1.add_subplot(212)
    #f2.plot(f[range(0,1000)], psdx[range(0,1000)])
    #f2.set_xlabel("Freq(Hz)")
    #fig1.show()
    #pdb.set_trace()

    return list(f),list(psdx)
