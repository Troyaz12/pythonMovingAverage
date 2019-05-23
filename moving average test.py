# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 07:30:12 2019

@author: Troy
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style 
import pandas as pd
import pandas_datareader.data as web
from tiingo import TiingoClient
import json
from pylab import *

newList = []
allDays = []
closingPrices = []
openingPrices = []
allDates = []
movingAverage = []
stockDictionary = {}
tickerstr = ""
config = {}
config['session'] = True
config['api_key'] = "8ed9ddaf35387e777893b1a084f1d8dbbefa7086"
action = 'buy'
amountInvested = 10000
date = '2007-12-21'

#aboveAverage = False
delayPeriod = 3         #delay period for buying or selling in days


client = TiingoClient(config)

start = dt.datetime(1993,2,1)
end = dt.datetime(2010,12,31)

def dayMovingAve(close):   
    total = 0
    length = len(close)
  
    for y in range(200,0,-1):
        total = close[y] + total
                  
    movingAverage1 = total/200
       
    for N in range(200,length):
        total = 0
        movingAverageSingleVal = 0
        end = N-200
        for y in range(N,end,-1):           
            total = close[y] + total
        
        movingAverageSingleVal = total/200        
        movingAverage.append(movingAverageSingleVal)
    
    for x in range(200,length):
        indexAve = x-200
        #clean up the date here before it goes into the list
        strDate = allDates[x]
        splitDate = strDate.rsplit("T")
        singleDate = splitDate[0]
        # add to dictionary
        tempDictionary = {singleDate: {'close':closingPrices[x],'open':openingPrices[x], 'average' : movingAverage[indexAve]}}
        stockDictionary.update(tempDictionary)
        
#is it above or below the moving average return buy or sell        
def movingAvePlacement(stockInfo,date):
 #   print (stockInfo.get(date))
 #   Mydata = {}
  #  myDictionary = {}
   # Mydata = stockInfo.get(date)
     
   # print(str(type(Mydata)))
 #   myDictionary = Mydata.items()
#    action = buySell(Mydata)
  #  print(str(action))
  #  return action

    for x,y in stockInfo.items():
                       #search dictionary for trade date
     #   print(str(x)+ " " + x + " " + str(y))                
        if x==date:    
            action = buySell(y)
         #   print(str(action))
            return action

###  analysis of moving average vs stock price determines if a buy or sell should be made
def buySell(stockdata):
   # print(str(type(stockdata)))
  #  print(str(stockdata))
    
    movingAverage = stockdata.get('average')
    stockPrice = stockdata.get('close')
   
    if(movingAverage>stockPrice):
        return "BUY"
    else:
        return "SELL"


## trade execution 
def trade (stockInfo, stockBuyDate, stockSellDate):
    isInvested = False
    dayMovingAve(closingPrices)         ##calc moving average and put all info in a dictionary of dictionaries
    
    
    for x,y in stockInfo.items():
        stockAction = movingAvePlacement(stockInfo, date)       #is it above or below the moving average
    
        if isInvested == False and stockAction == True:
            return False
            
        

ticker_price = client.get_ticker_price("SPY",fmt = "json", frequency = "weekly", startDate=start, endDate=end) #get json object

dictTicker = json.loads(json.dumps(ticker_price[:]))  #convert object to json and load in list as dictionary

for x in dictTicker:
    closingPrices.append(x["close"])
    openingPrices.append(x["open"])
    allDates.append(x["date"])
    

movingAvePlacement(stockDictionary, date)       #is it above or below the moving average
trade(stockDictionary,date,'2014-12-2')
#plt.plot(allDates,closingPrices)
#plt.plot(allDates, movingAverage)
#plt.title('Stock Price')
#plt.show()



    
#print(str(stockDictionary.keys()))   
                

