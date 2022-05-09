# Used libraries
from yahoo_fin.stock_info import get_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Apple Inc. market data
appl_data = get_data("aapl", start_date="01/01/2014", end_date="31/12/2019", index_as_date = True, interval="1d")
