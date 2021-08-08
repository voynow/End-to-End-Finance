import datetime

import numpy as np
import pandas_datareader.data as web
import matplotlib.pyplot as plt
plt.style.use('ggplot')

AAPL = web.DataReader(
	"AAPL", 
	'yahoo', 
	start='1990-01-01', 
	end=datetime.datetime.now())

MSFT = web.DataReader(
	"MSFT", 
	'yahoo', 
	start='1990-01-01', 
	end=datetime.datetime.now())

AMZN = web.DataReader(
	"IBM", 
	'yahoo', 
	start='1990-01-01', 
	end=datetime.datetime.now())

plt.plot(AAPL.index, np.log(AAPL["Close"].values), linewidth=1.5, label='AAPL')
plt.plot(MSFT.index, np.log(MSFT["Close"].values), linewidth=1.5, label='MSFT')
plt.plot(AMZN.index, np.log(AMZN["Close"].values), linewidth=1.5, label='IBM')
plt.legend()
plt.show()