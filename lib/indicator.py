import backtrader as bt
import os

class Stochastic_Generic(bt.Indicator):
    '''
    This generic indicator doesn't assume the data feed has the components
    ``high``, ``low`` and ``close``. It needs three data sources passed to it,
    which whill considered in that order. (following the OHLC standard naming)
    '''
    lines = ('k', 'd', 'dslow',)
    params = dict(
        pk=14,
        pd=3,
        pdslow=3,
        movav=bt.ind.SMA,
        slowav=None,
    )

    def __init__(self):
        # Get highest from period k from 1st data
        highest = bt.ind.Highest(self.data0, period=self.p.pk)
        # Get lowest from period k from 2nd data
        lowest = bt.ind.Lowest(self.data1, period=self.p.pk)

        # Apply the formula to get raw K
        kraw = 100.0 * (self.data2 - lowest) / (highest - lowest)

        # The standard k in the indicator is a smoothed versin of K
        self.l.k = k = self.p.movav(kraw, period=self.p.pd)

        # Smooth k => d
        slowav = self.p.slowav or self.p.movav  # chose slowav
        self.l.d = slowav(k, period=self.p.pdslow)


class MyStrategy(bt.Strategy):

    def __init__(self):

        self.ema1 = bt.indicators.ExponentialMovingAverage(self.data, period=self.ema1_val)
        self.ema2 = bt.indicators.ExponentialMovingAverage(self.data, period=self.ema2_val)
        self.ema3 = bt.indicators.ExponentialMovingAverage(self.data, period=self.ema3_val)
        
        self.rsi = Stochastic_Generic(self.data.high, self.data.low, self.data.close)

        self.long_signal = bt.And(
            self.last_price > self.ema1,
            self.ema1 > self.ema2,
            self.ema2 > self.ema3,
            self.rsi.l.k < self.RSI_FAST_MAX,
            self.rsi.l.d < self.self.rsi.l.k
        )
        self.short_signal = bt.And(
            self.last_price < self.ema1,
            self.ema1 < self.ema2,
            self.ema2 < self.ema3,
            self.rsi.l.d < self.RSI_SLOW_MIN,
            self.rsi.l.k < self.rsi.l.d
        )

    def log(self, status):
        file_name = 'log.txt'
        if not os.path.exists(file_name):
            with open(file_name, 'w') : pass
        with open(file_name, 'a') as f:
            f.write(status)
    
    def next(self):
        if self.data.close[0] == self.last_close:
            if self.long_signal:
                self.log('Long')

            if self.short_signal:
                self.log('Short')