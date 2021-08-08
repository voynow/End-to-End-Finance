import datetime

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
plt.style.use('ggplot')

import yfinance as yf

current_datetime = datetime.datetime.now()

symbols = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]["Symbol"].values

space = " "
symbols_string = space.join(symbols)
symbols_string = symbols_string.replace(".", "-")

data = yf.download(symbols_string, start='2000-01-01')