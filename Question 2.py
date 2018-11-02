from xlrd import open_workbook
import numpy as np
import statsmodels.api as sm
import pandas as pd
from pandas import Series, DataFrame
from xlrd import xldate_as_tuple 
import datetime

#importing the data from xlsx file
def read_from_excel():
    book = open_workbook('/Users/joyce/Desktop/Python/Python/Currencies.xlsx')
    sheet = book.sheet_by_index(0)
    dates = []
    BTC_prices = []
    ETH_prices = []
    XRP_prices = []
    Nasdaq_prices = []
    key_events = []
    LTC_prices = []
    LIBOR_rate = [] 
    for i in range(1,sheet.nrows):
        dates.append(datetime.datetime(*xldate_as_tuple(sheet.cell_value(i, 0), 0)).strftime('%Y/%d/%m'))
        BTC_prices.append(sheet.cell_value(i,1))
        key_events.append(sheet.cell_value(i,2))
        ETH_prices.append(sheet.cell_value(i,3))
        XRP_prices.append(sheet.cell_value(i,4))
        Nasdaq_prices.append(sheet.cell_value(i,5))
        LTC_prices.append(sheet.cell_value(i,6))
        LIBOR_rate.append(sheet.cell_value(i,7))
    return dates,BTC_prices,key_events,ETH_prices,XRP_prices,Nasdaq_prices,LTC_prices,LIBOR_rate
    

#2
def calculate_return_from_prices(input_prices):
    returns = []
    for i in range(1,len(input_prices)):
        log_price_in_position_i = np.log(input_prices[i])
        log_price_in_position_i1 = np.log(input_prices[i-1])
        return_in_position_i = log_price_in_position_i -log_price_in_position_i1
        returns.append(return_in_position_i)
    return returns

# delete all 0 prices from Nasdaq price, because there are only 252 working days on Nasdaq
def delete_0_nasdaq(key_events,nasdaq_prices):
    nasdaq = []
    nasdaq_keys = []
    for i in range(len(key_events)):
        if nasdaq_prices[i] != 0:
            nasdaq.append(nasdaq_prices[i])
            nasdaq_keys.append(key_events[i])
    return nasdaq_keys,nasdaq

def returns_on_key_events_dates(all_returns,key_events):
    #keep returns only for key events dates
    returns_on_key_events_dates = []
    for i in range(len(all_returns)):
        if key_events[i] == 1:
            returns_on_key_events_dates.append(all_returns[i])
    return returns_on_key_events_dates

def median_return_key(returns_on_key_events):
    N = len(returns_on_key_events)
    returns_on_key_events.sort()

    #find the length is even or odd
    if (N%2==0): #if even
        m1 = N/2
        m2 = (N/2)+1

    #Convert to integer
        m1 = int(m1)-1
        m2 = int(m2)-1
        median = (returns_on_key_events[m1]+returns_on_key_events[m2])/2

    else: #if odd
        m = (N+1)/2
        m = int(m)-1
        median = returns_on_key_events[m]

    return median

#according to the formula of standard deviation
#calculate its mean return and sum of list

def average_list(L1):
    average_list = sum(L1) / len(L1)
    return average_list

def variance_list(L1):
    average = average_list(L1)
    variance = 0
    for x in L1:
        diff_sq = (average-x)**2
        variance += diff_sq
    variance /= len(L1)
    return variance
    
def std_dev(L1):
    variance = variance_list(L1)
    return np.power(variance, 0.5)

def corr_x_y(x,y):
    n = len(x)
    #find the sum of products
    products = []
    for i, j in zip(x,y):
        products.append(i*j)
    sum_pro_x_y = sum(products)
    sum_x = sum(x)
    sum_y = sum(y)
    squared_sum_x = sum_x ** 2
    squared_sum_y = sum_y ** 2
    x_square = []
    for ii in x:
        x_square.append(ii**2)
    x_square_sum = sum(x_square)
    y_square = []
    for jj in y:
        y_square.append(jj**2)
    y_square_sum = sum(y_square)
    #use the formula to calculate
    numerator = n*sum_pro_x_y - sum_x*sum_y
    denominar_1 = n*x_square_sum-squared_sum_x
    denominar_2 = n*y_square_sum-squared_sum_y
    denominar = (denominar_1*denominar_2)**0.5
    correlation = numerator / denominar
    return correlation

def get_key_events(key_events):
    have_key_events = []
    for i in key_events:
        if i == 1:
            have_key_events.append(i)
    return have_key_events

def	calculate_regression(y,X):
    X = sm.add_constant(X)
    model = sm.OLS(y,X).fit()
#predictions = model.predict(X)
    result = model.summary()
    return result 
        

def delete_zero_rate(rates):
    rate = []
    for i in rates:
        if i != 0:
            rate.append(i)
    return rate

[dates,BTC_prices,key_events,ETH_prices,XRP_prices,Nasdaq_prices,LTC_prices, LIBOR_rate] = read_from_excel() #export data
have_key_events = get_key_events(key_events) #get the days that have key events
[Nasdaq_keys,Nasdaq] = delete_0_nasdaq(key_events,Nasdaq_prices)#delete all 0 prices from Nasdaq prices
return_on_all_BTC = calculate_return_from_prices(BTC_prices)
return_on_all_ETH = calculate_return_from_prices(ETH_prices)
return_on_all_XRP = calculate_return_from_prices(XRP_prices)

return_on_all_Nasdaq = calculate_return_from_prices(Nasdaq) #get all returns
return_on_key_events_BTC = returns_on_key_events_dates(return_on_all_BTC, key_events[1:])
return_on_key_events_ETH = returns_on_key_events_dates(return_on_all_ETH, key_events[1:])
return_on_key_events_XRP = returns_on_key_events_dates(return_on_all_XRP, key_events[1:])
return_on_key_events_Nasdaq = returns_on_key_events_dates(return_on_all_Nasdaq, Nasdaq_keys[1:])

#
#print average BTC return on the key events
print("The mean return on key events dates is:", average_list(return_on_key_events_BTC))
#print median return on key events
print("The median return on key events dates is", median_return_key(return_on_key_events_BTC))
#print standard deviation on key events
print("The standard deviation on key events dates is:", std_dev(return_on_key_events_BTC))

#correlation between key events variable and BTC
corr_btc_key = corr_x_y(key_events[1:],return_on_all_BTC)
print("The correlation between key events variable and BTC is:", corr_btc_key)
#correlation between key events variable and ETH
corr_eth_key = corr_x_y(key_events[1:],return_on_all_ETH)
print("The correlation between key events variable and ETH:", corr_eth_key)
#correlation between key events variable and XRP
corr_xrp_key = corr_x_y(key_events[1:],return_on_all_XRP)
print("The correlation between key events variable and XRP:", corr_xrp_key)
#correlation between key events variable and Nasdaq
corr_nas_key = corr_x_y(Nasdaq_keys[1:], return_on_all_Nasdaq)
print("The correlation between key events variable and Nasdaq:", corr_nas_key)
#
#x usually means our input variable in dataframe type
#x includes the the days that have key events and the returns of BTC, XRP, Nasdaq in key events days
X = DataFrame({"key_events": have_key_events, "BTC_events": return_on_key_events_BTC,
              "XRP_keys":return_on_key_events_XRP,"Nasdaq_keys":return_on_key_events_Nasdaq})

#y means dependent variable and the output
#y includes the return of ETH in key events days
y = return_on_key_events_ETH
print("The regression result is: \n", calculate_regression(y,X))


# Question 3
#rolling window is 15 days 
def calculate_mhist_volatility(portfolio_return):
    mhist_volatility = [] 
    for i in range(len(portfolio_return)):
        if i < 15:
            mhist_volatility.append('NON')# the first 15 data have no historical volatility
        else:
            mhist_volatility.append(std_dev(portfolio_return[i-15:i]))
    return mhist_volatility

def portfolio_daily_value(portfolio_price, start_price):
    portfolio_value = [start_price]
    for i in range(1, len(portfolio_price)):
        simple_rate = (portfolio_price[i] - portfolio_price[i-1])/portfolio_price[i-1]
        portfolio_value.append(portfolio_value[i-1]*(1+simple_rate))
    return portfolio_value
               
def assess_portfolio(date_range, symbols, portfolio_weights, start_value, risk_free_rate):
#dates list has two elements including start and end date
    df = pd.read_excel('/Users/joyce/Desktop/Python/Python/Currencies.xlsx')
    price_dates = {}
    Date = df['Date'].dt.strftime('%Y/%d/%m')
    #calculate daily return in the given time interval of each symbol
    for i in range(len(Date)):
        if Date[i] == date_range[0]: #Start_time and report its index
            j = i
            days = 0# calculate how many days in the time interval
            while Date[j] != date_range[1]:#until end date
                for k in range(len(symbols)):
                    if symbols[k] not in price_dates:
                        price_dates[symbols[k]] = [df[symbols[k]][j]]
                    else:
                        price_dates[symbols[k]].append(df[symbols[k]][j]) 
                j += 1
                days += 1
            for l in range(len(symbols)):
                price_dates[symbols[l]].append(df[symbols[l]][j]) #add end date data to each symbol
    return_daily = {}
    for k in range(len(symbols)):
        return_daily[symbols[k]] = calculate_return_from_prices(price_dates[symbols[k]])
   
    #calculate portfolio daily return in the given time interval
    portfolio_return = []
    portfolio_price = []
    for i in range(days):
        returns = 0
        prices = 0
        for j in range(len(symbols)):
            returns += return_daily[symbols[j]][i] * portfolio_weights[j]
            prices += price_dates[symbols[j]][i] * portfolio_weights[j]
        portfolio_return.append(returns)
        portfolio_price.append(prices)
    #calculate cumulative portfolio return in the time interval
    cumulative_return = np.sum(portfolio_return)
    #calculate the average period return
    average_return = np.mean(portfolio_return)
    #calculate Standard deviation of daily returns
    std_dev_return = std_dev(portfolio_return)
    #sharp_ratio = (expected portfolio return - risk_free rate) / standard deviation
    sharp_ratio = (cumulative_return - risk_free_rate)/std_dev_return
    # moving rolling window = 15
    mhist_volatility = calculate_mhist_volatility(portfolio_return)
    #calculate portfolio daily value
    end_value = portfolio_daily_value(portfolio_price, start_value)[-1]
    return portfolio_return,cumulative_return, average_return, std_dev_return,sharp_ratio, mhist_volatility,end_value
        
    
#    
return_on_all_LTC = calculate_return_from_prices(LTC_prices)   
#assess portfolio inputs
date_range = ['2017/15/02','2018/15/02']
symbols = ['BTC', 'ETH', 'XRP', 'LTC']
portfolio_weights = [0.2, 0.3, 0.4, 0.1]
start_value = 1000000
risk_free_rate = np.sum(LIBOR_rate)/252
[portfolio_return,cumulative_return, average_return, std_dev_return,sharp_ratio, mhist_volatility,end_value] = assess_portfolio(date_range,symbols,portfolio_weights,start_value,risk_free_rate)
print("The cumulative return is : %.5f" % cumulative_return)
print("The average period return is : %.5f" % average_return) 
print("The standard deviation of return is: %.5f" % std_dev_return)
print("The sharp ratio is: %.5f" % sharp_ratio)
volatility_frame = {'Date':dates[1:],'Moving Historical Volatility':mhist_volatility}
mhist_frame = pd.DataFrame(volatility_frame)
print("The mhist_volatility is \n", mhist_frame)
print("The ending value of the portfolio is %.5f" %end_value )



#Question 4


