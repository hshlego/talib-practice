import pandas as pd
import talib
import parser


def init_simple_moving_average(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:length]  # 종가를 범위만큼 불러와서 데이터프레임에 저장
    transactions_df['sma5'] = talib.SMA(close_list, 5)  # 5일선
    transactions_df['sma20'] = talib.SMA(close_list, 20)  # 20일선
    transactions_df.dropna(inplace=True)  # na값 드랍
    return transactions_df


def simple_moving_average(series: pd.Series, asset, budget, bought) -> (int, int, bool):
    if bought is False and series['sma5'] > series['sma20']:  # 매수 (전량 매수)
        bought = True
        asset = budget / series['close']
        budget = 0

    elif bought is True and series['sma5'] < series['sma20']:  # 매도 (전량 매도)
        bought = False
        budget = asset * series['close']
        asset = 0

    return asset, budget, bought


def init_weighted_moving_average(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:length]
    transactions_df['wma5'] = talib.WMA(close_list, 5)
    transactions_df['wma20'] = talib.WMA(close_list, 20)
    transactions_df.dropna(inplace=True)
    return transactions_df


def weighted_moving_average(series: pd.Series, asset, budget, bought) -> (int, int, bool):
    if bought is False and series['wma5'] > series['wma20']:  # 매수
        bought = True
        asset = budget / series['close']
        budget = 0

    elif bought is True and series['wma5'] < series['wma20']:  # 매도
        bought = False
        budget = asset * series['close']
        asset = 0

    return asset, budget, bought


def init_exponential_moving_average(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:length]
    transactions_df['ema5'] = talib.EMA(close_list, 5)
    transactions_df['ema20'] = talib.EMA(close_list, 20)
    transactions_df.dropna(inplace=True)
    return transactions_df


def exponential_moving_average(series: pd.Series, asset, budget, bought) -> (int, int, bool):
    if bought is False and series['ema5'] > series['ema20']:  # 매수
        bought = True
        asset = budget / series['close']
        budget = 0

    elif bought is True and series['ema5'] < series['ema20']:  # 매도
        bought = False
        budget = asset * series['close']
        asset = 0

    return asset, budget, bought
