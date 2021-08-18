""" These utility functions serve as the beginning of my applied financial utility suite. It may 
seem like there is no organization/documentation of these functions, and for now that is true. 
Sometime in the future when the repository is more mature and complex, developments will be made to 
organize and document. -voynow 8/15/2021 """

import numpy as np
import pandas as pd
import yfinance as yf

from datetime import datetime


def get_snp_data(size=None, start='2010-01-01', end=datetime.now()):

	wiki_snp_link = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

	# get current snp symbols
	snp_wiki = pd.read_html(wiki_snp_link)
	symbols = snp_wiki[0]['Symbol'].values

	# access random subset of snp symbols
	if size:
		random_idxs = np.random.choice(len(symbols), size=size, replace=False)
		symbols = symbols[random_idxs]

	# concatenate symbols into string for yfinance api
	space = " "
	symbols_string = space.join(symbols)
	symbols_string = symbols_string.replace(".", "-")

	# load data from 'start' to 'end' as specified by function params
	data = yf.download(symbols_string, start=start, end=end)

	return data


def remove_nan_cols(data, pct=.05):

	# Count number of nans in each row
	col_nan_counts = np.bincount(np.where(np.isnan(data.values))[1])

	# Find percentage of cols in DF with > 5% nan values
	nan_threshold = int(len(data) * pct)
	nan_col_idx = np.where(col_nan_counts > nan_threshold)[0]
	nan_cols = data.columns[nan_col_idx]
	data.drop(nan_cols, axis=1, inplace=True)

	return data


def get_asset_growth(data):

	# get close data
	close_data = data["Adj Close"]

	# find growth of assets over time interval
	growth = close_data.iloc[-1] / close_data.iloc[0]
	growth.dropna(inplace=True)
	sorted_growth = growth.iloc[np.argsort(growth.values)[::-1]]

	return sorted_growth


def normalize(data):

	universal_min_value = data - np.min(data)
	data_range = np.max(data) - np.min(data)

	return (universal_min_value / data_range)