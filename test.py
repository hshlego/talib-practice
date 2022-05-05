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
days = 180
fee = fees["binance"]*0.01

sma_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_simple_moving_average, strategy.simple_moving_average, fee)
print("sma profit :", sma_profit)

wma_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_weighted_moving_average, strategy.weighted_moving_average, fee)
print("wma profit :", wma_profit)

ema_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_exponential_moving_average, strategy.exponential_moving_average, fee)
print("ema profit :", ema_profit)

bbd_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_bollinger_bands, strategy.bollinger_bands, fee)
print("bbd profit :", bbd_profit)

johnbur_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_johnbur, strategy.johnbur, fee)
print("존버 profit :", johnbur_profit)