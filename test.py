import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import yfinance as yf

plt.style.use('ggplot')


# get current snp symbols
snp_wiki = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
symbols = snp_wiki[0]['Symbol'].values

# access random subset of snp symbols
size = 500
random_idxs = np.random.choice(len(symbols), size=size, replace=False)
symbols = symbols[random_idxs]

# concatenate symbols into string for yfinance api
space = " "
symbols_string = space.join(symbols)
symbols_string = symbols_string.replace(".", "-")

# load data from 2010 onward
start_date = '2010-01-01'
data = yf.download(symbols_string, start=start_date)

# Count number of nans in each row
col_nan_counts = np.bincount(np.where(np.isnan(data.values))[1])

# Find percentage of cols in DF with > 4% nan values (turns out this is only ~10-12% of all cols)
nan_col_idx = np.where(col_nan_counts > len(data) // 25)[0]
nan_cols = data.columns[nan_col_idx]
data.drop(nan_cols, axis=1, inplace=True)