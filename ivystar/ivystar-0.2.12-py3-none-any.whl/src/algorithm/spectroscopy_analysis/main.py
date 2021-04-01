import pandas as pd
import numpy as np
from Spectrum_analysis import spectrum
from Envelope_spectrum import envelope
from Power_spectrum_density import power
import pdb
import matplotlib.pylab as plt

# 读取文件
x = pd.read_csv('./122.csv')
x = np.array(x)             # 将读取的文件转换为数组
#x = np.delete(x,0,axis=0)   # 去掉第一行
x = np.delete(x,1,axis=1)   # 去掉第二列
x = x.astype(np.float64)    # 格式转为浮点数
x = np.ndarray.flatten(x)   # 将矩阵转换为一维数组

assert len(x) == 32768

# 采样频率Fs=25600,信号长度L=32768
# 频谱分析
S = spectrum(x,25600,32768)
print("Spectrum_analysis:")
print(S[0])
print(S[1])

# 包络谱分析
E = envelope(x,25600,32768)
print("Envelope_spectrum:")
print(E[0])
print(E[1])

# 功率谱分析
P = power(x,25600,32768)
print("Power_spectrum_density :")
print(P[0])
print(P[1])

