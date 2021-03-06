# -*- coding: utf-8 -*-
"""SMA_tradingIndicator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IYiAwYYhepBw0sb-CCy_BKtb93giVeMv
"""

# This programm uses a dual moving average crosspver to determine when t buy and sell stock

#Import the libraries
import pandas as pd
import numpy as np
from datetime import datetime 
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Load data
# TODO Get Live Data from API
from google.colab import files
uploaded = files.upload();

# Store the data
# Implement more crypto currencies
BTC = pd.read_csv('Bitbay_BTCUSD_1h_1.csv')
#Show the data:
BTC

#Visualize chart data
plt.figure(figsize=(12.5, 4.5))
plt.plot(BTC['Close'], label = 'BTC')
plt.title('BTC Adj. close price history')
plt.xlabel('2020-10-12, 12 pm -> now')
plt.ylabel('Closed Price USD')
plt.legend(loc='upper left')
plt.plot()
plt.gca().invert_xaxis() # plot from old date to recent date
plt.show()

# Create a simple moving average with 30 day window
SMA500 = pd.DataFrame()
SMA500['Close'] = BTC['Close'].rolling(window = 500).mean()
SMA500

#Create a simple 100 day moving average
SMA1500 = pd.DataFrame()
SMA1500['Close'] = BTC['Close'].rolling(window = 1500).mean()
SMA1500

#Visualize SMA
plt.figure(figsize=(12.5, 4.5))
plt.plot(BTC['Close'], label = 'BTC')
plt.plot(SMA500['Close'], label = 'SMA500')
plt.plot(SMA1500['Close'], label = 'SMA1500')
plt.title('BTC Adj. close price history')
plt.xlabel('2020-10-12, 12 pm -> now')
plt.ylabel('Closed Price USD')
plt.legend(loc='upper left')
plt.plot()
plt.gca().invert_xaxis() # plot from old date to recent date
plt.show()

# Create nw Data Frame to store the data
data = pd.DataFrame()
data['BTC'] = BTC['Close']
data['SMA500'] = SMA500['Close']
data['SMA1500'] = SMA1500['Close']
data

# Function to signal when to buy and sell the asset

def buy_sell(data):
  sigPriceBuy = []
  sigPriceSell = []
  flag = -1

  for i in range(len(data)):
    if data['SMA500'][i] > data['SMA1500'][i]:
      if flag != 1:
        sigPriceBuy.append(data['BTC'][i])
        sigPriceSell.append(np.nan)
        flag = 1
      else:
        sigPriceBuy.append(np.nan)
        sigPriceSell.append(np.nan)
    elif data['SMA500'][i] < data['SMA1500'][i]:
      if flag != 0:
        sigPriceBuy.append(np.nan) 
        sigPriceSell.append(data['BTC'][i])
        flag = 0
      else:
          sigPriceBuy.append(np.nan)
          sigPriceSell.append(np.nan)
    else:
          sigPriceBuy.append(np.nan)
          sigPriceSell.append(np.nan)

  return (sigPriceBuy, sigPriceSell)

# Store buy and sell data points
buy_sell = buy_sell(data)
data['Buy_Signal_price'] = buy_sell[0]
data['Sell_Signal_price'] = buy_sell[1]

# Show data
data

# Visualize data and strategy to sell and buy 
plt.figure(figsize = (12.5, 4.6))
plt.plot(data['BTC'], label = 'BTC', alpha = 0.35)
plt.plot(data['SMA500'], label = 'SMA500', alpha = 0.35)
plt.plot(data['SMA1500'], label = 'SMA1500', alpha = 0.35)
plt.scatter(data.index, data['Buy_Signal_price'], label = 'buy', marker = '^', color = 'green')
plt.scatter(data.index, data['Sell_Signal_price'], label = 'sell', marker = 'v', color = 'red')
plt.title('BTC Close Price History Buy & Sell Signals')
plt.xlabel("timeframe")
plt.ylabel('Close USD')
plt.legend(loc='upper right')
plt.plot()
plt.gca().invert_xaxis() # plot from old date to recent date
plt.show()