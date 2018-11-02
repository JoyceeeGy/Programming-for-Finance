import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# read data from excel as Dataframe type
df = pd.read_excel('C:/Users/feife/Desktop/Cryptocurrencies_prices_3.xlsx', index_col=0)
# calculate daily price change rate for BTC and ETH
# price change = (daily price - daily price of last day) / daily price of last day
df['BTC_price_change'] = (df['BTC_Prices'] - df['BTC_Prices'].shift(1)) / df['BTC_Prices'].shift(1)
df['ETH_price_change'] = (df['ETH_Prices'] - df['ETH_Prices'].shift(1)) / df['ETH_Prices'].shift(1)
# calculate log return of BTC/ETH
df['BTC_return'] = np.log(df['BTC_Prices'] / df['BTC_Prices'].shift(1))
df['ETH_return'] = np.log(df['ETH_Prices'] / df['ETH_Prices'].shift(1))
# assume weight of BTC and ETH are both 0.5
weights = [0.5, 0.5]
# daily portfolio return = [BTC return, ETH return] * [weights]
df['portfolio_return'] = df['BTC_return'] * weights[0] + df['ETH_return'] * weights[1]

# define function to deal with market events
# if daily price change is lower than -15%, position of next day doubles
def sign_modify_by_market_events(currency_signs):
    currency = currency_signs.split('_')[0]
    price_change = '%s_price_change' % currency # get price change for BTC and ETH
    for i in range(0, len(df[currency_signs])):
        if df[price_change][i] <= -0.15:
            df[currency_signs][i] *= (-2) # double the position

BTC_cols = []
ETH_cols = []
# define daily position for BTC/ETH
# daily position = the sign of the mean price change in previous 3,5,8,10 days
for i in [3, 5, 8, 10]:
    BTC_col = 'BTC_position_%s' % i
    ETH_col = 'ETH_position_%s' % i
    df[BTC_col] = np.sign(df['BTC_price_change'].rolling(i).mean())
    df[ETH_col] = np.sign(df['ETH_price_change'].rolling(i).mean())
    sign_modify_by_market_events(BTC_col) # modify the position by market events
    sign_modify_by_market_events(ETH_col) # modify the position by market events
    BTC_cols.append(BTC_col)
    ETH_cols.append(ETH_col)

sns.set()
strats = ['portfolio_return']
# calculate daily portfolio return based on postion
for col in BTC_cols:
    strat = 'strategy_%s' % col.split('_')[2]
    BTC_var = 'BTC_position_%s' % col.split('_')[2]
    ETH_var = 'ETH_position_%s' % col.split('_')[2]
    df[strat] = df[BTC_var].shift(1) * df['BTC_return'] * weights[0] + df[ETH_var].shift(1) * df['ETH_return'] * weights[1]
    strats.append(strat)
df[strats].cumsum().plot() # plot the cumsum portfolio return
plt.show() # display the plot

