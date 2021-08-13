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

