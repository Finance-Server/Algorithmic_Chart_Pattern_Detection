import pandas as pd 
import numpy as np 
from scipy.signal import argrelextrema
from statsmodels.nonparametric.kernel_regression import KernelReg
import matplotlib.pyplot as plt

data = pd.read_csv('AAPL.csv', ',')
data.set_index('Date', inplace=True)

####################################################################
# Find the price high and lows using scipy.signal.argregexterma.   #
####################################################################

'''
Args : argrelextrema takes in an an ndarray and a comparable. The comparables we’ll use will be np.greater and np.less. 

Returns :  a tuple with an array of the results. 
'''

local_max = argrelextrema(data['High'].values, np.greater)[0]
local_min = argrelextrema(data['Low'].values, np.less)[0]

highs = data.iloc[local_max,:]
lows = data.iloc[local_min,:]


##################################################################
# Smoothing the Noise - Reducing the noise in the price action   #
##################################################################

# fig = plt.figure(figsize = [20, 14])
# data['Close'].plot()
# data['Close'].rolling(window = 5).mean().plot()
# plt.show()

###############################################################################
# Non-Parametric Kernel Regression - Reducing the noise in the price action   #
###############################################################################

'''
Non-parametric kernel regression is another way to smooth our prices. The idea is that we approximate a price average 
based on prices near the predicted price using a weighting the closest prices more heavily.
'''

kr = KernelReg(data['Close'], data.index, var_type='c', bw=[1])
kr2 = KernelReg(data['Close'].values, data.index, var_type='c', bw=[3])
f = kr.fit([data['Close'].values])
f2 = kr2.fit([data['Close'].values])

smooth_prices = pd.Series(data=f[0], index=data.index)
smooth_prices2 = pd.Series(data=f2[0], index=data.index)
smooth_prices.plot()
smooth_prices2.plot()
