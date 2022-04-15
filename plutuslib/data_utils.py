from typing import List
import requests as req
import pandas as pd
from datetime import datetime as dt

from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

endpoint_url = 'https://ftx.com/api/markets'
daily = str(60*60*24) # for resolution param in req header
start_date = dt(2015, 1, 1).timestamp()

def get_top_ftx_mkts(n, type):
    """Returns FTX top n markets
    :param n: top n markets, sorted by 24h vol
    :type n: int
    :param type: either 'spot' or 'future'
    :type type: str
    :returns: a list of tickers for top n markets of the specified type (spot/perpetual)
    :rtype: list
    """
    historical_data = req.get(f'{endpoint_url}').json()
    df = pd.DataFrame(historical_data['result'])
    df = df[df['type'] == type]
    if type == "future":
        df = df[df['name'].str.contains("PERP")]
    else:
        df = df[df['name'].str.contains("USDT") == False] # don't want USDT pairs, only USD
        df = df[df['name'].str.contains("USD")]
    df = df.sort_values(by=['volumeUsd24h'], ascending=False).reset_index(drop=True)
    
    return list(df.head(n)['name'])

def get_ftx_df():
    """Grabs the OHLCV historical data for each of the top n ftx markets, and returns a consolidated df
    :returns:
        - df - consolidated dataframe containing OHLCV data
        - instruments - list of symbols
    """
    ohlcvs = {}
    symbols = get_top_ftx_mkts(100, 'spot')

    for symbol in symbols:
        historical_data = req.get(f'{endpoint_url}/{symbol}/candles?resolution={daily}&start_time={start_date}').json()
        symbol_df = pd.DataFrame(historical_data['result'])
        symbol_df['startTime'] = pd.to_datetime(symbol_df['startTime']).dt.date
        symbol_df = symbol_df.set_index('startTime')
        #we are interested in the OHLCV mainly, let's rename them 
        ohlcvs[symbol] = symbol_df[["open", "high", "low", "close", "volume"]]
        # print(symbol)
        # print(ohlcvs[symbol]) #we can now get the data that we want inside a nicely formatted df
    
    #now, we want to put that all into a single dataframe.
    #since the columns need to be unique to identify the instrument, we want to add an identifier.
    #let's steal the GOOGL index as our dataframe index
    df = pd.DataFrame(index=ohlcvs["BTC/USD"].index)
    df.index.name = "date"
    instruments = list(ohlcvs.keys())

    for inst in instruments:
        inst_df = ohlcvs[inst]
        columns = list(map(lambda x: "{} {}".format(inst, x), inst_df.columns)) #this tranforms open, high... to AAPL open , AAPL high and so on
        df[columns] = inst_df

    return df, instruments

def extend_dataframe(traded, df):
    """Takes in a list of symbols and a dataframe to fill in missing data, and generate new data as well
    :param traded: list of symbols in the df
    :param df: pandas dataframe containing OHLCV data
    :returns: historical_data contains new df w/ filled data, and new columns
    :rtype: pd.Dataframe
    
    """
    open_cols = list(map(lambda x: str(x) + " open", traded))
    high_cols = list(map(lambda x: str(x) + " high", traded))
    low_cols = list(map(lambda x: str(x) + " low", traded))
    close_cols = list(map(lambda x: str(x) + " close", traded))
    volume_cols = list(map(lambda x: str(x) + " volume", traded))

    historical_data = df.copy()
    historical_data = historical_data[open_cols + high_cols + low_cols + close_cols + volume_cols]
    
    historical_data.fillna(method="ffill", inplace=True)
    historical_data.fillna(method="bfill", inplace=True)

    for inst in traded:
        historical_data[f'{inst} % ret'] = historical_data[f'{inst} close'] / historical_data[f'{inst} close'].shift(1)
        historical_data[f'{inst} % ret vol'] = historical_data[f'{inst} % ret'].rolling(25).std()
        historical_data[f'{inst} active'] = historical_data[f'{inst} close'] != historical_data[f'{inst} close'].shift(1)
    return historical_data

