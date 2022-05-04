import csv_parser
from backtest import backtest
import strategy

btc = csv_parser.get_dataframe()
budget = 1_000_000
start = 0
days = 7
fee = 0.00
sma_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_simple_moving_average, strategy.simple_moving_average, fee)
print("sma profit :", sma_profit)

wma_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_weighted_moving_average, strategy.weighted_moving_average, fee)
print("wma profit :", wma_profit)

ema_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_exponential_moving_average, strategy.exponential_moving_average, fee)
print("ema profit :", ema_profit)

johnbur_profit = backtest(btc, 1_000_000, start, days*24, strategy.init_johnbur, strategy.johnbur, 0.05)
print("존버 profit :", johnbur_profit)