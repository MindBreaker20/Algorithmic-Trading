# Used libraries
from yahoo_fin.stock_info import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Apple Inc. market data
appl_data = get_data("aapl", start_date="01/01/2014", end_date="31/12/2019", index_as_date = True, interval="1d")

# Exponentially Weighted Moving Average
def ewma(data_set, n): # there are two arguments data frame column, which represents Close prce and n, which is time horizon
    alpha = 2 / (n + 1) # alpha
    window = [] # window is a list, where calculated EWMAs are stored
    ewm_1 = data_set[n] # on the beginning of calculation the EWMA does not exist so the last closing price from time horizon is used
    window.append(ewm_1) # adding the first evma
    for i in range(0, len(data_set) - n): # this loop represents how many times this 'rolling window' can be performed in given time interval
        ewm_i = alpha * data_set[i + n] + (1 - alpha) * window[i] # EWMA equation
        window.append(ewm_i) # adding calculated EWMA to the list
    return window # returning the list of calculated EWMA

# Calculating short and long EWMA (20 and 50 days)
ewma_daily_20 = ewma(appl_data['close'], 20) 
ewma_daily_50 = ewma(appl_data['close'], 50)

# Empty columns need to be created as there is need to present short and long EWMa on the timeseries
appl_data['ewma_20'] = np.nan 
appl_data['ewma_50'] = np.nan

# Populating new columns with EWMA values from lists
for i in range(0, len(appl_data['close']) - 20):
    appl_data['ewma_20'][i + 20] = ewma_daily_20[i]

for i in range(0, len(appl_data['close']) - 50):
    appl_data['ewma_50'][i + 50] = ewma_daily_50[i]
    
# Calculating trade signals (0 - sell asset, 1 - buy asset)
appl_data['signal'] = 0.0
appl_data['signal'][20:] = np.where(appl_data['ewma_40'][20:] > appl_data['ewma_100'][20:], 1.0, 0.0)
appl_data['position'] = appl_data['signal'].diff()

# Visualization
fig = plt.figure(figsize = (20, 15))
ax1 = fig.add_subplot(111, ylabel='Price in $')
appl_data['close'].plot(ax=ax1, color='black', lw = 2.)
appl_data[['ewma_40', 'ewma_100']].plot(ax=ax1, lw=2.)
ax1.plot(appl_data.loc[appl_data.position == 1.0].index, appl_data.ewma_40[appl_data.position == 1.0], '^',
         markersize = 20, color='g')

ax1.plot(appl_data.loc[appl_data.position == -1.0].index, appl_data.ewma_40[appl_data.position == -1.0], 'v',
         markersize = 20, color='r')
