import threading
from . import api, indicator, send_email
import os
import backtrader as bt

class Filter(threading.Thread):
    
    def __init__(self, mode, timeframe):
        threading.Thread.__init__(self)
        self.mode = mode
        self.timeframe = timeframe
        self.robot = api.API(mode=self.mode, timeframe=self.timeframe)
    
    def read_log(self):
        file_name = 'log.txt'
        if not os.path.exists(file_name):
            with open(file_name, 'w') : pass
        with open(file_name, 'r') as f:
            try:
                last_line = f.readlines()[-1].rstrip('\n')
            except:
                return False
            else:
                open(file_name, 'w').close()
                return last_line
    
    def run(self):
        while True:
            coin_lsit = self.robot.get_list()
            cerebro = bt.Cerebro()
            for coin in coin_lsit:
                data, last_price = self.robot.get_kline(coin)

                cerebro.broker.set_cash(60000)
                cerebro.adddata(data)

                indicator.MyStrategy.ema1_val = 50
                indicator.MyStrategy.ema2_val = 100
                indicator.MyStrategy.ema3_val = 200
                indicator.MyStrategy.RSI_FAST_MAX = 80
                indicator.MyStrategy.RSI_SLOW_MIN = 20
                
                indicator.MyStrategy.last_price = last_price
                cerebro.addstrategy(indicator.MyStrategy)
                cerebro.run()
                
                result = self.read_log()
                if result or result != '':
                    if result == 'Long':
                        send_email.send_mail(coin, 'LONG')
                    if result == 'Short':
                        send_email.send_mail(coin, 'SHORT')