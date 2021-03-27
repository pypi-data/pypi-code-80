# %%
import warnings

from datetime import datetime

import math
from math import pow

import itertools
import numpy as np

import scipy as sp
import scipy.fftpack 

import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import sklearn.metrics
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

from statsmodels.tsa.stattools import adfuller

import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout  
from tensorflow.keras import regularizers
from tensorflow.keras import initializers

plt.style.use('default')

# %%
l2 = regularizers.l2

# %%
def create_dataset(dataset, look_back=1):

	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)

def unseason(ts, length):
  avgSeason = average_season(ts)
  avgSeasons = np.tile(avgSeason,22)
  return -1 * avgSeasons[:length]

def average_season(ts):
  return np.array(ts.groupby([ts.index.month,ts.index.day]).mean())

def differencing(data, periods):
  """Docstring for differencing
  we take the difference of the observation at a particular instant with that at the previous instant
  
  Parameters 
  ----------
  data : Dataframe
  periods : int
  Number of periods to shift. Can be positive or negative.

  Returns
  -------
  Dataframe plot
  """
  data_log = np.log(data)
  data_log_diff = data_log-data_log.shift(periods=periods)
  return plt.plot(data_diff)

def moving_average(ts,window):
    """ we take average of ‘k’ consecutive values depending on the frequency of time series

    Parameters
    ----------
    ts : dataframe
    window : int
    Size of the moving window. This is the number of observations used for calculating the statistic. Each window will be a fixed size.

    Returns
    -------
    a Window or Rolling sub-classed for the mean
    """

    ts_log  = np.log(ts)
    rolling_mean = ts_log.rolling(window = window , center = False).mean()
    ts_log_rolling_mean_diff = ts_log - rolling_mean
    ts_log_rolling_mean_diff.dropna(inplace = True)
    
    return ts_log_rolling_mean_diff  
# %%
class Flood():

  """docstring for ClassName"""
  def __init__(self,file_name):
    self.file_name = file_name
    

  def data(self,file_name):
    data_to_load = files.upload()
    #for google colab 
    self.data = pd.read_csv(io.BytesIO(data_to_load[self.file_name]),parse_dates=['Date'], index_col='Date')
    print(self.data)

  def normalized_features(self,data):

    self.dataset = self.data.values  # .as_matrix() will be decrepit in the future, switched to .values
    scaler = MinMaxScaler(feature_range=(0, 1))
    self.dataset = scaler.fit_transform(self.dataset) #fit scaler
    print(self.dataset)
  
  def split(self,dataset, ratio):
    
    self.train_size = int(len(dataset) * (ratio * .01))
    self.test_size = len(dataset) - self.train_size
    print(len(data))
    self.train, self.test = dataset[0:self.train_size,:], dataset[self.train_size:len(dataset),:]
    print("train size: {} and test size : {}".format(self.train_size,self.test_size))

  def test_stationarity(self,timeseries):
    
    #Determing rolling statistics
    rolmean = timeseries.rolling(window=365,center=False).mean()
    rolstd = timeseries.rolling(window=365,center=False).std()

    #Plot rolling statistics:
    plt.figure(figsize=(15,8))
    orig = plt.plot(timeseries,label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation ')
    plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)  

     
  def ANN_model(self, train, test, train_size, data ,look_back = 1 ):

      
    plt.style.use('default')

    # %%
    l2 = regularizers.l2
    dataset = data.values  # .as_matrix() will be decrepit in the future, switched to .values
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset) #fit scaler
    # reshape into X=t and Y=t+1
    # lookback is the window size
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    print(data)

    # %%
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    
    # %%
    # numEpoch: number of passes through the data

    numEpoch = 100
    vl_splt = 730.0 / 5475.0
    initBias = initializers.glorot_uniform(seed=0)
    initKernel = initializers.Orthogonal(gain=1.0, seed=0)


    # %%
    # create and fit the dense ann
    # first we need to flatten the extra dimension within the dataset
    flat_TrainX = np.reshape(trainX, (4910, look_back))
    #print(testX.shape)
    flat_TestX = np.reshape(testX, (1623, 20))
    #print(flat_TestX.shape)

    # %%
    ann = Sequential()

    ann.add(Dense(10, input_shape=(look_back,),
                    kernel_initializer = initKernel, 
                    bias_initializer = initBias, name='d1'),
              )

    ann.add(Dense(1, kernel_initializer = initKernel,
                    bias_initializer = initBias,
                    kernel_regularizer=l2(0.01),
                    bias_regularizer=l2(0.01)))

    ann.compile(loss='mean_squared_error', optimizer='adam')

    ann.fit(flat_TrainX, trainY, epochs=numEpoch, batch_size=1,
              verbose=2, validation_split = vl_splt)

    # %%
      
    ##Test Model
      

    # %%
    trainY = scaler.inverse_transform([trainY])
    testY = scaler.inverse_transform([testY])

    # %%
    # make predictions
    ann_trainPredict = ann.predict(flat_TrainX)
    ann_testPredict = ann.predict(flat_TestX)
    # invert predictions
    ann_trainPredict = scaler.inverse_transform(ann_trainPredict)
    ann_testPredict = scaler.inverse_transform(ann_testPredict)

    # calculate root mean squared error
    ann_trainScore = math.sqrt(mean_squared_error(trainY[0], ann_trainPredict[:,0]))
    #print('Train Score: %.2f RMSE' % (ann_trainScore))
    ann_testScore = math.sqrt(mean_squared_error(testY[0], ann_testPredict[:,0]))
    print('Test Score: %.2f RMSE' % (ann_testScore))

    # normalized RMSE
    y_min, y_max  =  min(trainY[0]), max(trainY[0])
    yhat = y_max - y_min
    print("Normalized RMSE: %s" % (ann_testScore/yhat))

    # %%
    # shift train predictions for plotting
    ann_trainPredictPlot = np.empty_like(dataset)
    ann_trainPredictPlot[:, :] = np.nan
    ann_trainPredictPlot[look_back:len(ann_trainPredict)+look_back, :] = ann_trainPredict
    # shift test predictions for plotting
    ann_testPredictPlot = np.empty_like(dataset)
    ann_testPredictPlot[:, :] = np.nan
    ann_testPredictPlot[len(ann_trainPredict)+
                          (look_back*2)+1:len(dataset)-1, :] = ann_testPredict

    # plot baseline and predictions
    plt.figure(figsize=(18,8))
    #plt.plot(scaler.inverse_transform(dataset))
    #plt.plot(ann_trainPredictPlot)

    dates = data.index[train_size:-1].values

    ann_testPredictPlot = [ann_testPredictPlot[i][0] for i in range(train_size+1, len(ann_testPredictPlot))]

    pred = pd.DataFrame({"Date": dates, "Volume": ann_testPredictPlot})
    pred.Date = pd.to_datetime(pred.Date)
    pred.set_index("Date", inplace=True)

    plt.title("Water Volume (seasoned predictions)")
    plt.plot(data)
    plt.plot(pred)
    plt.show()

  def LSTM_model(self, tain, test, train_size, data, look_back = 1):
    plt.style.use('default')

    # %%
    l2 = regularizers.l2
    dataset = data.values  # .as_matrix() will be decrepit in the future, switched to .values
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset) #fit scaler
    # reshape into X=t and Y=t+1
    # lookback is the window size
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    print(data)

    # %%
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    # %%
    
    ##Train Model
   

    # %%
    
    # %%
    # numEpoch: number of passes through the data

    numEpoch = 100
    vl_splt = 730.0 / 5475.0
    initBias = initializers.glorot_uniform(seed=0)
    initKernel = initializers.Orthogonal(gain=1.0, seed=0)


    # %%
    # first we need to flatten the extra dimension within the dataset
    flat_TrainX = np.reshape(trainX, (5727, look_back))
    #print(testX.shape)
    flat_TestX = np.reshape(testX, (1896, 20))
    #print(flat_TestX.shape)

    # %%
    # create and fit the LSTM
    lstm = Sequential()

    lstm.add(LSTM(8, input_shape=(1, look_back), 
                  kernel_initializer = initKernel, 
                  bias_initializer = initBias,
                  kernel_regularizer=l2(0.00001),
                 # recurrent_regularizer=l2(0.0001),
                        
                  bias_regularizer=l2(0.00001),
                  dropout=0.01,
                 #recurrent_dropout=0.01
                 ))


    lstm.add(Dense(1, kernel_initializer = initKernel, 
                   bias_initializer = initBias,
                 #  kernel_regularizer=l2(0.01),
                  # bias_regularizer=l2(0.01)
                  ))

    lstm.compile(loss='mean_squared_error', 
                 optimizer='adam')

    lstm.fit(trainX, trainY, epochs=numEpoch, batch_size=1, 
             verbose=2, validation_split = vl_splt)

    # %%
 
    ##Test Model
    

    # %%
    trainY = scaler.inverse_transform([trainY])
    testY = scaler.inverse_transform([testY])

    # %%
    # make predictions
    lstm_trainPredict = lstm.predict(trainX)
    lstm_testPredict = lstm.predict(testX)
    # invert predictions
    lstm_trainPredict = scaler.inverse_transform(lstm_trainPredict)
    lstm_testPredict = scaler.inverse_transform(lstm_testPredict)

    # calculate root mean squared error
    lstm_trainScore = math.sqrt(mean_squared_error(trainY[0], lstm_trainPredict[:,0]))
    #print('Train Score: %.2f RMSE' % (lstm_trainScore))
    lstm_testScore = math.sqrt(mean_squared_error(testY[0], lstm_testPredict[:,0]))
    print('Test Score: %.2f RMSE' % (lstm_testScore))

    y_min, y_max  =  min(trainY[0]), max(trainY[0])
    yhat = y_max - y_min
    print("Normalized RMSE: %s" % (lstm_testScore/yhat))

    # %%
    # shift train predictions for plotting
    lstm_trainPredictPlot = np.empty_like(dataset)
    lstm_trainPredictPlot[:, :] = np.nan
    lstm_trainPredictPlot[look_back:len(lstm_trainPredict)+look_back, :] = lstm_trainPredict
    # shift test predictions for plotting
    lstm_testPredictPlot = np.empty_like(dataset)
    lstm_testPredictPlot[:, :] = np.nan
    lstm_testPredictPlot[len(lstm_trainPredict)+
                        (look_back*2)+1:len(dataset)-1, :] = lstm_testPredict

    # plot baseline and predictions
    plt.figure(figsize=(18,8))
    #plt.plot(scaler.inverse_transform(dataset))
    #plt.plot(lstm_trainPredictPlot)


    dates = data.index[train_size:-1].values

    lstm_testPredictPlot = [lstm_testPredictPlot[i][0] for i in range(train_size+1, len(lstm_testPredictPlot))]
    pred = pd.DataFrame({"Date": dates, "Volume": lstm_testPredictPlot})
    pred.Date = pd.to_datetime(pred.Date)
    pred.set_index("Date", inplace=True)

    plt.plot(data)
    plt.plot(pred)
    plt.title("Water Volume (seasoned predictions)")
    plt.show()

  def RNN_model(self, train, test, train_size, data, look_back = 1):
    plt.style.use('default')

    # %%
    l2 = regularizers.l2
    dataset = data.values  # .as_matrix() will be decrepit in the future, switched to .values
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset) #fit scaler
    # reshape into X=t and Y=t+1
    # lookback is the window size
    trainX, trainY = create_dataset(train, look_back)
    testX, testY = create_dataset(test, look_back)
    print(data)

    # %%
    # reshape input to be [samples, time steps, features]
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))

    # %%
   
    ##Train Model
    
    # %%
    # numEpoch: number of passes through the data

    numEpoch = 100
    vl_splt = 730.0 / 5475.0
    initBias = initializers.glorot_uniform(seed=0)
    initKernel = initializers.Orthogonal(gain=1.0, seed=0)


    # %%
    # create and fit the dense ann
    # first we need to flatten the extra dimension within the dataset
    flat_TrainX = np.reshape(trainX, (5727, look_back))
    #print(testX.shape)
    flat_TestX = np.reshape(testX, (1896, 20))
    #print(flat_TestX.shape)

    # %%
    # create and fit the simpleRNN
    simpleRNN = Sequential()
    simpleRNN.add(SimpleRNN(8, 
                            input_shape=(1, look_back),
                            kernel_initializer = initKernel, 
                            bias_initializer = initBias,
                           # kernel_regularizer=l2(0.00001),
                           # recurrent_regularizer=l2(0.0001),
                            
                           bias_regularizer=l2(0.00001),
                           dropout=0.01,
                           #recurrent_dropout=0.01
                           ))


    simpleRNN.add(Dense(1, 
                        kernel_initializer = initKernel, 
                        bias_initializer = initBias
                       # kernel_regularizer=l2(0.001),
                    #    bias_regularizer=l2(0.001)
                       ))

    simpleRNN.compile(loss='mean_squared_error', optimizer='adam')
    simpleRNN.fit(trainX, trainY, epochs=numEpoch, 
                  batch_size=1, verbose=2, validation_split = vl_splt) #look into setting validation set

    # %%
    
    ##Test Model
   

    # %%
    trainY = scaler.inverse_transform([trainY])
    testY = scaler.inverse_transform([testY])

    # %%
    # make predictions
    RNN_trainPredict = simpleRNN.predict(trainX)
    RNN_testPredict = simpleRNN.predict(testX)
    # invert predictions
    RNN_trainPredict = scaler.inverse_transform(RNN_trainPredict)
    RNN_testPredict = scaler.inverse_transform(RNN_testPredict)

    # calculate root mean squared error
    RNN_trainScore = math.sqrt(mean_squared_error(trainY[0], RNN_trainPredict[:,0]))
    #print('Train Score: %.2f RMSE' % (RNN_trainScore))
    RNN_testScore = math.sqrt(mean_squared_error(testY[0], RNN_testPredict[:,0]))
    print('Test Score: %.2f RMSE' % (RNN_testScore))

    # normalized RMSE
    y_min, y_max  =  min(trainY[0]), max(trainY[0])
    yhat = y_max - y_min
    print("Normalized RMSE: %s" % (RNN_testScore/yhat))

    # %%
    # shift train predictions for plotting
    RNN_trainPredictPlot = np.empty_like(dataset)
    RNN_trainPredictPlot[:, :] = np.nan
    RNN_trainPredictPlot[look_back:len(RNN_trainPredict)+look_back, :] = RNN_trainPredict
    # shift test predictions for plotting
    RNN_testPredictPlot = np.empty_like(dataset)
    RNN_testPredictPlot[:, :] = np.nan
    RNN_testPredictPlot[len(RNN_trainPredict)+
                        (look_back*2)+1:len(dataset)-1, :] = RNN_testPredict

    # plot baseline and predictions
    plt.figure(figsize=(18,8))
    #plt.plot(scaler.inverse_transform(dataset))
    #plt.plot(RNN_trainPredictPlot)


    dates = data.index[train_size:-1].values

    RNN_testPredictPlot = [RNN_testPredictPlot[i][0] for i in range(train_size+1, len(RNN_testPredictPlot))]
    pred = pd.DataFrame({"Date": dates, "Volume": RNN_testPredictPlot})
    pred.Date = pd.to_datetime(pred.Date)
    pred.set_index("Date", inplace=True)

    plt.title("Water Volume (seasoned predictions)")
    plt.plot(data)
    plt.plot(pred)
    plt.show()



    






