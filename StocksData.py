from datetime import datetime as dt, timedelta
from stocks import Stocks
import pandas as pd
from nsepython import *

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

def trimDF(df):
    selectedColumns = ['CH_SYMBOL','CH_TRADE_HIGH_PRICE','CH_TRADE_LOW_PRICE','CH_PREVIOUS_CLS_PRICE','CH_OPENING_PRICE','CH_CLOSING_PRICE','mTIMESTAMP']
    res = df[selectedColumns].tail(2)
    new_column_names = {'CH_SYMBOL': 'STOCK', 'CH_TRADE_HIGH_PRICE':'DAY HIGH','CH_TRADE_LOW_PRICE': 'DAY LOW', 'mTIMESTAMP':'DATE','CH_OPENING_PRICE' : 'OPEN PRICE', 'CH_CLOSING_PRICE' : 'CLOSE PRICE',
						'CH_LAST_TRADED_PRICE' : 'LTP', 'CH_PREVIOUS_CLS_PRICE':'PREVIOUS CLOSE'}
    res.rename(columns=new_column_names,inplace=True)

    return res

def filterdf(selectedCandlePattern,result):
    if selectedCandlePattern == 'bullishEngulfing':
        for quote in result.keys():
            df = trimDF(result[quote])
            print(df)
        return "Checking for pattern " + selectedCandlePattern
    elif selectedCandlePattern == 'bullishHammer':
        return "Checking for pattern " + selectedCandlePattern     


def screenCandlePattern(selectedSector,selectedCandlePattern):
    
    quotes = Stocks(selectedSector).getQuotes()
    result = {}
    endDate = dt.now()
    startDate = endDate - timedelta(days=10)
    dateRange = getDateRange(startDate=startDate,endDate=endDate)

    for quote in quotes:
        data = getStocksData(quote=quote,dateRange=dateRange)
        if type(data) == int:
            print("Couldn't fetch for quote:",quote)
            continue
        else: result[quote] = data

    res = filterdf(selectedCandlePattern,result)

    return res


