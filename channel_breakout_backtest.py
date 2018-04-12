# -*- coding: utf-8 -*-
import pandas as pd
from backtest import Backtest, BacktestReport

def highest(series, window):
    return series.rolling(window).max()

def lowest(series, window):
	return series.rolling(window).min()

# テストデータ読み込み
data = pd.read_csv('bitmex_20180410_1m.csv', index_col='timestamp', parse_dates=True)
print(data.head())

# インジケーター作成
breakout_in = 22
breakout_out = 5

long_entry_price = highest(data.high, breakout_in)
short_entry_price = lowest(data.low, breakout_in)

long_exit_price = lowest(data.low, breakout_out)
short_exit_price = highest(data.high, breakout_out)

# エントリー／イグジット
long_entry = data.close > long_entry_price.shift(1)
short_entry = data.close < short_entry_price.shift(1)
long_exit = data.close < long_exit_price.shift(1)
short_exit = data.close > short_exit_price.shift(1)

long_entry[:breakout_in] = False
short_entry[:breakout_in] = False
long_exit[:breakout_out] = False
short_exit[:breakout_out] = False

# バックテスト実施
# entry_exit = pd.DataFrame({'close':data.close, 'open':data.open,
# 	'long_entry_price':long_entry_price, 'long_exit_price':long_exit_price, 'long_entry':long_entry, 'long_exit':long_exit,
# 	'short_entry_price':short_entry_price, 'short_entry':short_entry, 'short_exit_price':short_exit_price, 'short_exit':short_exit}, index=data.index)
# print(entry_exit.to_csv())

(Trades, PL) = Backtest(data, long_entry, long_exit, short_entry, short_exit, lots=1)
Equity = BacktestReport(Trades, PL)