import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from full_fred.fred import Fred
import time

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

#Set a time period for the chart
start_date = '2003-01-01'
end_date = '2023-09-01'
#Get S&P500 price data from yfinance
df_spx = yf.download('^GSPC', start=start_date, end=end_date)

#Use your own API Key, create a txt file named 'key.txt' which stores your own api key
fred = Fred('key.txt')

#Create a dictionary containing the data that you want to get and plot from FRED
#Below are 4 sample data points from FRED
fred_name_dict = {'T10Y2Y': 'Treasury 10 vs 2',
                  'CPIAUCSL': 'CPI',
                  'UNRATE': 'Unemployment rate',
                  'M2SL': 'M2'}

for fred_code, fred_name in fred_name_dict.items():
#Get the data and clean the data
    df = fred.get_series_df(fred_code)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.set_index('date')

    df = df[df['value'] != '.']
    df['value'] = df['value'].astype(float)
    df = df[['value']]

    df = df[df.index >= start_date]
    df = df[df.index <= end_date]

#Plot the chart
    sns.set_theme(style='darkgrid')
    fig, ax1 = plt.subplots(figsize=(10,6))
    sns.lineplot(data=df_spx['Close'], ax=ax1, color='indigo')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('SP500', color='indigo')
    ax1.tick_params('y', colors='indigo')

    ax2 = ax1.twinx()
    sns.lineplot(data=df['value'], ax=ax2, color='grey')
    ax2.set_ylabel(fred_name, color='grey')
    ax2.tick_params('y', colors='grey')
    title='SP500 vs '+ fred_name
    plt.title(title)
    plt.show()

#Below is for getting and plotting a single chart
# df = fred.get_series_df('T10Y2Y')
# df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
# df = df.set_index('date')
#
# df = df[df['value'] != '.']
# df['value'] = df['value'].astype(float)
# df = df[['value']]
#
# df = df[df.index >= start_date]
# df = df[df.index <= end_date]
#
# sns.set_theme(style='darkgrid')
# fig, ax1 = plt.subplots(figsize=(10,6))
# sns.lineplot(data=df_spx['Close'], ax=ax1, color='indigo')
# ax1.set_xlabel('Date')
# ax1.set_ylabel('SP500', color='indigo')
# ax1.tick_params('y', colors='indigo')
#
# ax2 = ax1.twinx()
# sns.lineplot(data=df['value'], ax=ax2, color='grey')
# ax2.set_ylabel('T10Y2Y', color='grey')
# ax2.tick_params('y', colors='grey')
# title = 'SP500 vs '+ 'T10Y2Y'
# plt.title(title)
# plt.show()
