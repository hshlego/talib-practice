import csv_parser
from backtest import backtest
import strategy

fees = {
    "upbit": 0.05,
    "binance": 0.1
}

btc = csv_parser.get_dataframe()
budget = 1_000_000
start = 0
days = 30
fee = fees["binance"]*0.01

sma_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_simple_moving_average, strategy.simple_moving_average, fee)
print("sma profit : {:.3f}".format(sma_profit))

wma_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_weighted_moving_average, strategy.weighted_moving_average, fee)
print("wma profit : {:.3f}".format(wma_profit))

ema_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_exponential_moving_average, strategy.exponential_moving_average, fee)
print("ema profit : {:.3f}".format(ema_profit))

bbd_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_bollinger_bands, strategy.bollinger_bands, fee)
print("bbd profit : {:.3f}".format(bbd_profit))

env_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_envelope, strategy.envelope, fee)
print("env profit : {:.3f}".format(env_profit))

rsi_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_rsi, strategy.rsi, fee)
print("rsi profit : {:.3f}".format(rsi_profit))

macd_histogram_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_macd_histogram, strategy.macd_histogram, fee)
print("macd histrogram profit : {:.3f}".format(macd_histogram_profit))

macd_signal_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_macd_signal, strategy.macd_signal, fee)
print("macd signal profit : {:.3f}".format(macd_signal_profit))

stoch_slow_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_stoch_slow, strategy.stoch_slow, fee)
print("stoch slow profit : {:.3f}".format(stoch_slow_profit))

stoch_fast_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_stoch_fast, strategy.stoch_fast, fee)
print("stoch fast profit : {:.3f}".format(stoch_fast_profit))

johnbur_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_johnbur, strategy.johnbur, fee)
print("jbr profit : {:.3f}".format(johnbur_profit))