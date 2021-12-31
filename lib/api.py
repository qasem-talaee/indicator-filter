import requests
import pandas as pd
import time
import backtrader as bt

class API:
    
    def __init__(self, mode, timeframe):
        ### f = Futures , e = Exchange
        self.mode = mode
        self.timeframe = timeframe
    
    def get_kline(self, market):
        flag = True
        while flag:
            try:
                df = requests.get("https://api.coinex.com/v1/market/kline?market={market}&type={timeframe}&limit=1000".format(market=market, timeframe=self.timeframe))
            except:
                flag = True
            else:
                flag = False
                time.sleep(5)
        df = pd.json_normalize(df.json(), ['data'])
        df.columns = ['time', 'open', 'close', 'high', 'low', 'trade_vol', 'trade_val']
        df = df.drop(['trade_vol', 'trade_val'], axis=1)
        df.drop(df.tail(1).index,inplace=True)
        df = df.reset_index()
        df = df.drop('index', axis=1)
        df = df.astype({"open": float, "close": float, "high": float, "low": float})
        last_close = df['close'].iloc[-1]
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])

        data = bt.feeds.PandasData(dataname=df, datetime=0, open=1, high=3, low=4, close=2, volume=None, openinterest=None, nocase=None)
        return data, last_close
    
    def get_list(self):
        if self.mode == 'f':
            data = requests.get("https://api.coinex.com/perpetual/v1/market/list")
            data = data.json()['data']
            coin = []
            for i in range(len(data)):
                if data[i]['name'][-1] == 'T':
                    coin.append(data[i]['name'])
            return coin

        if self.mode == 'e':
            data = requests.get("https://api.coinex.com/v1/market/list")
            data = data.json()['data']
            coin = []
            for i in range(len(data)):
                if data[i][-1] == 'T':
                    coin.append(data[i])
            return coin
