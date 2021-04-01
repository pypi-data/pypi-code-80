# 频谱分析
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pdb

def spectrum(x,Fs,L):
    '''
    x 数据
    Fs 采样频率
    L 时间
    '''
    T = 1/Fs                    # 采样时间 多少次采样是1秒钟
    t = np.arange(L)/Fs         # 时间向量 传入的整体数据是几个1秒钟
    y = x-np.mean(x)            # 零均值化

    # 绘图,画出信号时域图像
    #fig = plt.figure()
    #fig.tight_layout()#调整整体空白
    #plt.subplots_adjust(wspace =0, hspace =.5)#调整子图间距
    #f = fig.add_subplot()
    #f.plot(t,y)
    #f.set_ylim(-25,25)
    #f.set_xlabel('time (seconds)')
    #fig.show()
    # 绘图结束

    # 傅里叶变换
    NFFT = L
    # np.fft.fft，对输入信号进行快速傅里叶变换,输出长度与输入相同
    Y = np.fft.fft(y)
    A = 2*abs(Y)/NFFT         # 转换为幅值     
    A = A[range(int(L/2)+1)]  # 单边频谱,由于对称性，只取一半区间
    f = Fs/2*np.linspace(0, 1, NFFT//2+1)    # 横坐标，频率

    #绘图显示结果
    fig1 = plt.figure()
    fig1.tight_layout()#调整整体空白
    plt.subplots_adjust(wspace =0, hspace =.5)#调整子图间距
    f1 = fig1.add_subplot(211)
    f1.plot(f,A)
    f1.set_xlabel('Frequency (Hz)')
    f1.set_title('Single-Sided Amplitude Spectrum of y(t)')
    f2 = fig1.add_subplot(212)
    f2.plot(f[range(0,1000)], A[range(0,1000)])
    f2.set_xlabel("Freq(Hz)")
    # fig1.show()
    # pdb.set_trace()
    # 绘图结束
    return  list(f),list(A)

