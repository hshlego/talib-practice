from strategy import *
import csv_parser
from backtest import backtest
from queue import PriorityQueue
import json
from datetime import date


class Algo:
    def __init__(self, name, profit):
        self.name = name
        self.profit = profit

    def __lt__(self,other):
        return self.profit > other.profit


method_list = [
    ["단순이평선 교차", init_simple_moving_average, simple_moving_average],
    ["가중이평선 교차", init_weighted_moving_average, weighted_moving_average],
    ["지수이평선 교차", init_exponential_moving_average, exponential_moving_average],
    ["볼린저 밴드", init_bollinger_bands, bollinger_bands],
    ["Envelope", init_envelope, envelope, envelope],
    ["RSI", init_rsi, rsi],
    ["CCI", init_cci, cci],
    ["MACD 히스토그램", init_macd_histogram, macd_histogram],
    ["MACD 기준선", init_macd_signal, macd_signal],
    ["Stochastic Slow", init_stoch_slow, stoch_slow],
    ["Stochastic Fast", init_stoch_fast, stoch_fast],
]

fees = {
    "free": 0,
    "upbit": 0.05,
    "binance": 0.1,
}

coin_list = csv_parser.get_all_coin_dataframe()
days_list = [7, 30, 180, 365]
fee = fees['binance'] * 0.01

id = 0
output_list = []
for coin in coin_list:
    for days in days_list:
        print(coin["name"], days)

        pq = PriorityQueue()
        for method in method_list:
            name = method[0]
            init_method = method[1]
            actual_method = method[2]

            profit = backtest(coin['dataframe'], 1_000_000, 0, days*24, init_method, actual_method, fee)
            pq.put(Algo(name, profit))

        ranks = []
        profits = []
        for i in range(4):
            algo = pq.get()
            ranks.append(algo.name)
            profits.append("+{:.2f}%".format((algo.profit-1)*100))

        output_list.append({'id': id, 'ranks': ranks, 'profits': profits})
        id += 1

json_path = './jsons/' + str(date.today()) + '.json'
with open(json_path, 'w') as outfile:
    json.dump(output_list, outfile, ensure_ascii=False, indent=4)