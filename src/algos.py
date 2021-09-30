import numpy as np
import json, requests, datetime, timedelta

from constants import api_url, coin, ids
from orders import sell_order, get_price

class stop_loss:

    def __init__(self, start_bal, auth):
        # start_bal is xlm balance 
        # in usd or is 0
        self.start_bal = start_bal
        self.auth = auth

    # call to check if stop loss is needed
    def __call__(self):
        total = 0
        s = requests.get(api_url + 'accounts/'+ids.xlm,auth=self.auth).json()
        # current total balance in usd
        total = ( float(s['balance']) * float(get_price(self.auth)) )
        
        if self.start_bal == 0:
            return

        # if current holding is down 10% trigger stop loss
        if (float(self.start_bal)*0.9) >= total:
            sell_order(self.auth, self)
            print("stop loss sell")
        
    # update value after buy or sell
    def update(self, new_val):
        self.start_bal = new_val
        
# simple rsi calculation
def calculate_rsi(auth):
    # get current time and convert to gmt
    end = datetime.datetime.now() + datetime.timedelta(hours=4)
    start = (end - datetime.timedelta(minutes=15)).isoformat()
    end = end.isoformat()
    # get closing prices of xlm for the past 14 minutes
    r = requests.get(api_url + 'products/'+coin+'/candles?start='+start+'&end='+end+'&granularity=60',auth=auth).json()
    arr = []
    for x in r:
        arr.append(x[4])
    #reverse because most recent values are posted first
    arr.reverse()
    #convert into numpy array b/c its cool
    closing_prices = np.array(arr)
    
    i = 0
    length = len(closing_prices) - 1
    avg_gain = avg_loss = 0
    #iterate over the array to calculate avg gain/avg loss
    while i < length:
        diff = closing_prices[i] - closing_prices[i+1]
        if diff < 0:
            avg_gain += (diff*(-1))
        else:
            avg_loss += diff
        i += 1
    avg_gain /= 14
    avg_loss /= 14
    
    rsi = 0
    try:
        rsi = 100 - (100 / (1 + (avg_gain/avg_loss)))
    except ZeroDivisionError:
        print('error')
    return rsi



'''
def cal culate_sma(auth):
    # get current time and convert to gmt
    end = datetime.datetime.now() + datetime.timedelta(hours=4)
    start = (end - datetime.timedelta(minutes=60)).isoformat()
    end = end.isoformat()
    # get closing prices of xlm for the past 70 minutes
    r = requests.get(api_url + 'products/'+coin+'/candles?start='+start+'&end='+end+'&granularity=60',auth=auth).json()
    arr = []
    for x in r:
        arr.append(x[4])
    #convert into numpy array b/c its cool
    closing_prices = np.array(arr)
    return np.average(closing_prices)
'''    