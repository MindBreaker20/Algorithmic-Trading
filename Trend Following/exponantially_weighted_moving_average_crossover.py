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
  
