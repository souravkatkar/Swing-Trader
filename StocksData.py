from datetime import datetime as dt, timedelta
from stocks import Stocks
import pandas as pd
from nsepython import *
import time
import math

def getDateRange(startDate,endDate):
    '''Gets the start date and end date and returns the string dateRange in the required format for web scraping'''
    startDate = startDate.strftime("%d-%m-%Y")
    endDate = endDate.strftime("%d-%m-%Y")
    return "from={0}&to={1}".format(startDate,endDate)    


def getStocksData(quote,dateRange):
    '''will get the data for a stock for the given dateRange'''
    url="https://www.nseindia.com/api/historical/securityArchives?{0}&symbol={1}&dataType=priceVolumeDeliverable&series=EQ".format(dateRange,quote)
    print(url)
    try:
        responseData = nsefetch(url)
        data=responseData["data"]
        res = pd.DataFrame(data)
        return res
    except Exception as e:
        print("Failed to fetch for {0} with error {1}".format(quote,e))
        return 0

def trimWebData(webData):
    for quote in webData.keys():
        #print(quote)
        selectedColumns = ['CH_SYMBOL','CH_TRADE_HIGH_PRICE','CH_TRADE_LOW_PRICE','CH_PREVIOUS_CLS_PRICE','CH_OPENING_PRICE','CH_CLOSING_PRICE','mTIMESTAMP']
        data = webData[quote]
        #print(data[selectedColumns].tail(2))
        new_column_names = {'CH_SYMBOL': 'STOCK', 'CH_TRADE_HIGH_PRICE':'DAY HIGH','CH_TRADE_LOW_PRICE': 'DAY LOW', 'mTIMESTAMP':'DATE','CH_OPENING_PRICE' : 'OPEN PRICE', 'CH_CLOSING_PRICE' : 'CLOSE PRICE',
                             'CH_LAST_TRADED_PRICE' : 'LTP', 'CH_PREVIOUS_CLS_PRICE':'PREVIOUS CLOSE'}
        data.rename(columns=new_column_names,inplace=True)
        webData[quote] = data

    return webData


def getWebData(selectedSector):
    
    quotes = Stocks(selectedSector).getQuotes()
    result = {}
    endDate = dt.now()
    startDate = endDate - timedelta(days=10)
    dateRange = getDateRange(startDate=startDate,endDate=endDate)

    for quote in quotes:
        time.sleep(1)
        data = getStocksData(quote=quote,dateRange=dateRange)
        if type(data) == int:
            print("Couldn't fetch for quote:",quote)
            continue
        else: result[quote] = data

    return result


def screenCandle(webData,selectedCandlePattern):
    print("Inside screenCandle")
    data = trimWebData(webData=webData)
    result = []
    if selectedCandlePattern == 'bullishHammer':
        for quote in data.keys():
            lastDayData = data[quote].tail(1).iloc[0]
            
            openPrice, closePrice, dayHigh, dayLow = lastDayData['OPEN PRICE'], lastDayData['CLOSE PRICE'], lastDayData['DAY HIGH'], lastDayData['DAY LOW']

            totalRange = dayHigh - dayLow
            bodyRange = abs(closePrice-openPrice)
            levelPrice = dayHigh - 0.6 * totalRange

            if (bodyRange * 4 <= totalRange) and (closePrice >= levelPrice)  and (openPrice >= levelPrice):
                result.append(quote)

    elif selectedCandlePattern == 'bullishEngulfing':
        for quote in data.keys():
            requiredData = data[quote].tail(2)
            lastDayData = requiredData.iloc[1]
            openPrice, closePrice, dayHigh, dayLow = lastDayData['OPEN PRICE'], lastDayData['CLOSE PRICE'], lastDayData['DAY HIGH'], lastDayData['DAY LOW']
            bodyHigh = max(openPrice,closePrice)
            bodyLow = min(openPrice,closePrice)

            
            last2ndData = requiredData.iloc[0]
            openPrice2, closePrice2, dayHigh2, dayLow2 = last2ndData['OPEN PRICE'], last2ndData['CLOSE PRICE'], last2ndData['DAY HIGH'], last2ndData['DAY LOW']
            bodyHigh2 = max(openPrice2,closePrice2)
            bodyLow2 = min(openPrice2,closePrice2)

            if bodyLow < bodyLow2 and bodyHigh > bodyHigh2 and dayHigh > dayHigh2 and dayLow < dayLow2:
                if openPrice < closePrice:
                    result.append(quote)


            
    print(result)

    return result
