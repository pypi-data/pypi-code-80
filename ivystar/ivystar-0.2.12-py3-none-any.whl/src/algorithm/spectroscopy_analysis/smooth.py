#!

'''
smoother 将离散的采样结果，进行平滑处理
line_diff 两组采样数据间的MSE MAE R2 pearsonr
'''
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.signal
import sklearn
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error # 均方误差
from sklearn.metrics import mean_absolute_error # 平方绝对误差
from sklearn.metrics import r2_score # R square
from scipy.interpolate import splint
import numpy as np
from scipy.interpolate import make_interp_spline

def line_diff(x, y):
    '''
    求见两组采样结果的多个参数，评估两组结果的相似程度
    x,y 两组list数据，尺寸对齐
    '''
    _pearsonr = pearsonr(x,y)
    _mse = mean_squared_error(x,y)
    _mae = mean_absolute_error(x,y)
    _r2 = r2_score(x,y)
    return {"pearsonr":_pearsonr,"mse":_mse,"mae":_mae,"r2":_r2}

def smoother(x, window_len, times, mode='nearest'):
    '''
    取平滑会失去信息，导致波形失真
    x 输入的list数据
    window_len 滑动窗口长度，平滑的导数取多远
    times 平滑方程的指数，曲率
    mode 模式
    '''
    y = scipy.signal.savgol_filter(x,window_len,times)
    return y

def spline(x, y):
    '''
    平滑波形
    '''
    x_smooth = np.linspace(min(x),max(x), max(x)*10) #300 represents number of points to make between T.min and T.max
    power_smooth = make_interp_spline(np.array(x), np.array(y))(x_smooth)
    return power_smooth

def draw_lines(x_lst, save_or_show='show'):
    '''
    绘制多路时序信号
    '''
    fig = plt.figure() # 绘图
    fig.tight_layout() # 紧凑布局
    plt.subplots_adjust(wspace =0, hspace =.5) # 调整子图行列间距
    x_lst_len = len(x_lst)
    for index, i in enumerate(x_lst):
        horiz = "%d1%d"%(x_lst_len, index+1)
        f1 = fig.add_subplot(int(horiz))
        f1.plot([index for index,_ in enumerate(i)], i)
        f1.set_xlabel('Time')
        f1.set_title('The %d data'%index)
    if save_or_show == 'show':
        fig.show()
        import pdb
        pdb.set_trace()
    else:
        fig.savefig("./tmp.jpg")
    return 0

if __name__ == "__main__":
    df = pd.read_csv("122.csv")
    _z = list(df.iloc[:,0].values)[:20]
    _o = list(df.iloc[:,1].values)[:20]
    _p = smoother(_z, 3, 2, mode='nearest')
    _q = spline([index for index,_ in enumerate(_z)], _z)
    df = line_diff(_q, _z)
    draw_lines([_z,_o,_p,_q],"show")
    print(df)


