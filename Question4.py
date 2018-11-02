import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#reading data from excel
df = pd.read_excel('/Users/joyce/Desktop/Python/Python/Currencies.xlsx')
#choose BTC and ETH cryptocurrencies.
#calculate their log returns
df['BTC_log_return'] = np.log(df['BTC']/df['BTC'].shift(1))
df['ETH_log_return'] = np.log(df['ETH']/df['ETH'].shift(1))
#get the portfolio return, assume equal weights
df['portfolio_return'] = df['BTC_log_return'] * 0.5 + df['ETH_log_return'] * 0.5
#calculate their daily returns
df['BTC_daily_returns'] = (df['BTC']-df['BTC'].shift(1))/df['BTC'].shift(1)
df['ETH_daily_returns'] = (df['ETH']-df['ETH'].shift(1))/df['ETH'].shift(1)

#specific market event
#daily return is lower than -15%, then triple their positions
def spf_market_event(currencies):
    currency = currencies.split('_')[0]
    returns = '%s_daily_returns' % currency
    for i in range(len(df[currencies])):
        if df[returns][i] <= -0.15:
            df[currencies][i] *= (-3)



#momentuam strategy by using previous 1,7,14,30 days
BTC_cols = []
ETH_cols = []
for momentum in [1,7,14,30]:
    BTC_col = 'BTC_position_%s' % momentum
    ETH_col = 'ETH_position %s' % momentum
    df[BTC_col] = np.sign(df['BTC_daily_returns'].rolling(momentum).mean())
    df[ETH_col] = np.sign(df['ETH_daily_returns'].rolling(momentum).mean())
    spf_market_event(BTC_col)
    spf_market_event(ETH_col) #results from market events
    BTC_cols.append(BTC_col)
    ETH_cols.append(ETH_col)


    
#to derive the absolute performance of the momentum strategy for the different momentum intervals(in days)
sns.set()
strats = ['portfolio_return']
# calculate daily portfolio return based on postion
for col in BTC_cols:
    strat = 'strategy_%s' % col.split('_')[2]
    BTC_c = 'BTC_position_%s' % col.split('_')[2]
    ETH_c = 'ETH_position_%s' % col.split('_')[2]
    df[strat] = df[BTC_c].shift(1) * df['BTC_log_return'] * 0.5 + df[ETH_c].shift(1) * df['ETH_log_return'] * 0.5
    strats.append(strat)
df[strats].cumsum().plot() 
plt.show() 

    