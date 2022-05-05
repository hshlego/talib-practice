from pickle import HIGHEST_PROTOCOL
from typing import Tuple
import pandas as pd
import talib
import csv_parser


def init_simple_moving_average(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]  # 종가를 범위만큼 불러와서 데이터프레임에 저장
    transactions_df['sma5'] = talib.SMA(close_list, 5)  # 5일선
    transactions_df['sma20'] = talib.SMA(close_list, 20)  # 20일선
    transactions_df.dropna(inplace=True)  # na값 드랍
    return transactions_df


def simple_moving_average(series: pd.Series, asset, budget, bought, fee) -> Tuple[int, int, bool]:
    if bought is False and series['sma5'] > series['sma20']:  # 매수 (전량 매수)
        bought = True
        budget *= (1 - fee)
        asset = budget / series['close']
        budget = 0

    elif bought is True and series['sma5'] < series['sma20']:  # 매도 (전량 매도)
        bought = False
        budget = asset * series['close']
        budget *= (1 - fee)
        asset = 0

    return asset, budget, bought


def init_weighted_moving_average(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['wma5'] = talib.WMA(close_list, 5)
    transactions_df['wma20'] = talib.WMA(close_list, 20)
    transactions_df.dropna(inplace=True)
    return transactions_df


def weighted_moving_average(series: pd.Series, asset, budget, bought, fee) -> Tuple[int, int, bool]:
    if bought is False and series['wma5'] > series['wma20']:  # 매수
        bought = True
        budget *= (1 - fee)
        asset = budget / series['close']
        budget = 0

    elif bought is True and series['wma5'] < series['wma20']:  # 매도
        bought = False
        budget = asset * series['close']
        budget *= (1 - fee)
        asset = 0

    return asset, budget, bought


def init_exponential_moving_average(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['ema5'] = talib.EMA(close_list, 5)
    transactions_df['ema20'] = talib.EMA(close_list, 20)
    transactions_df.dropna(inplace=True)
    return transactions_df


def exponential_moving_average(series: pd.Series, asset, budget, bought, fee) -> Tuple[int, int, bool]:
    if bought is False and series['ema5'] > series['ema20']:  # 매수
        bought = True
        budget *= (1 - fee)
        asset = budget / series['close']
        budget = 0

    elif bought is True and series['ema5'] < series['ema20']:  # 매도
        bought = False
        budget = asset * series['close']
        budget *= (1 - fee)
        asset = 0

    return asset, budget, bought


def init_johnbur(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    return transactions_df


def johnbur(series: pd.Series, asset, budget, bought, fee) -> Tuple[int, int, bool]:
    if bought is False:
        bought = True
        budget *= (1 - fee)
        asset = budget / series['close']
        budget = 0

    return asset, budget, bought


def init_bollinger_bands(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    upper, middle, lower = talib.BBANDS(close_list, matype=talib.MA_Type.T3)
    transactions_df['bbands_upper'] = upper
    transactions_df['bbands_middle'] = middle
    transactions_df['bbands_lower'] = lower
    transactions_df.dropna(inplace=True)
    return transactions_df


def bollinger_bands(series: pd.Series, asset, budget, in_band, fee) -> Tuple[int, int, bool]:
    if not in_band:
        if series['bbands_lower'] < series['close']:  # BUY
            in_band = True
            amount = budget / 4
            asset += amount * (1 - fee) / series['close']
            budget -= amount
        elif series['bbands_upper'] > series['close']:  # SELL
            in_band = True
            amount = asset / 4
            asset -= amount
            budget += amount * series['close'] * (1 - fee)
    else:
        if series['bbands_lower'] > series['close']:  # Got out of the band
            in_band = False
        elif series['bbands_upper'] < series['close']:  # Got out of the band
            in_band = False

    return asset, budget, in_band


def init_envelope(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['ema20'] = talib.EMA(close_list, 20)
    transactions_df.dropna(inplace=True)
    return transactions_df


def envelope(series: pd.Series, asset, budget, in_band, fee) -> Tuple[int, int, bool]:
    thickness = 0.2
    low_frac = 1 - thickness
    high_frac = 1 + thickness
    if not in_band:
        if series['ema20'] * low_frac < series['close']:  # BUY
            in_band = True
            amount = budget / 4
            asset += amount * (1 - fee) / series['close']
            budget -= amount
        elif series['ema20'] * high_frac > series['close']:  # SELL
            in_band = True
            amount = asset / 4
            asset -= amount
            budget += amount * series['close'] * (1 - fee)
    else:
        if series['ema20'] * low_frac > series['close']:  # Got out of the band
            in_band = False
        elif series['ema20'] * high_frac < series['close']:  # Got out of the band
            in_band = False

    return asset, budget, in_band


def init_rsi(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['rsi'] = talib.RSI(close_list)
    transactions_df.dropna(inplace=True)
    return transactions_df


def rsi(series: pd.Series, asset, budget, in_band, fee) -> Tuple[int, int, bool]:
    lower_bound = 70
    upper_bound = 30
    if not in_band:
        if lower_bound < series['rsi']:  # BUY
            in_band = True
            amount = budget / 4
            asset += amount * (1 - fee) / series['close']
            budget -= amount
        elif upper_bound > series['rsi']:  # SELL
            in_band = True
            amount = asset / 4
            asset -= amount
            budget += amount * series['close'] * (1 - fee)
    else:
        if lower_bound > series['rsi']:  # Got out of the band
            in_band = False
        elif upper_bound < series['rsi']:  # Got out of the band
            in_band = False

    return asset, budget, in_band


def init_cci(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    high_list = csv_parser.get_nparray(df, 'high', start, length)
    low_list = csv_parser.get_nparray(df, 'low', start, length)
    close_list = csv_parser.get_nparray(df, 'close', start, length)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['cci'] = talib.CCI(high_list, low_list, close_list)
    transactions_df.dropna(inplace=True)
    return transactions_df


def cci(series: pd.Series, asset, budget, in_band, fee) -> Tuple[int, int, bool]:
    lower_bound = 100
    upper_bound = -100
    if not in_band:
        if lower_bound < series['cci']:  # BUY
            in_band = True
            amount = budget / 4
            asset += amount * (1 - fee) / series['close']
            budget -= amount
        elif upper_bound > series['cci']:  # SELL
            in_band = True
            amount = asset / 4
            asset -= amount
            budget += amount * series['close'] * (1 - fee)
    else:
        if lower_bound > series['cci']:  # Got out of the band
            in_band = False
        elif upper_bound < series['cci']:  # Got out of the band
            in_band = False

    return asset, budget, in_band


def init_macd_histogram(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)
    macd, macd_signal, macd_histogram = talib.MACD(close_list, 12, 26, 9)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['histogram'] = macd_histogram
    transactions_df.dropna(inplace=True)
    return transactions_df


def macd_histogram(series: pd.Series, asset, budget, bought, fee) -> Tuple[int, int, bool]:
    if bought is False and series['histogram'] > 0:  # BUY
        bought = True
        asset = budget * (1 - fee) / series['close']
        budget = 0

    elif bought is True and series['histogram'] < 0:  # SELL
        bought = False
        budget = asset * series['close'] * (1 - fee)
        asset = 0

    return asset, budget, bought


def init_macd_signal(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    close_list = csv_parser.get_nparray(df, 'close', start, length)
    macd, macd_signal, macd_hist = talib.MACD(close_list, 12, 26, 9)

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['signal'] = macd_signal
    transactions_df.dropna(inplace=True)
    return transactions_df


def macd_signal(series: pd.Series, asset, budget, bought, fee) -> Tuple[int, int, bool]:
    if bought is False and series['signal'] > 0:  # BUY
        bought = True
        asset = budget * (1 - fee) / series['close']
        budget = 0

    elif bought is True and series['signal'] < 0:  # SELL
        bought = False
        budget = asset * series['close'] * (1 - fee)
        asset = 0

    return asset, budget, bought


def init_stoch_slow(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    high_list = csv_parser.get_nparray(df, 'high', start, length)
    low_list = csv_parser.get_nparray(df, 'low', start, length)
    close_list = csv_parser.get_nparray(df, 'close', start, length)
    slowk, slowd = talib.STOCH(high_list, low_list, close_list, 10, 6, 0, 6, 0)  # high, low, close, fastk_period, slowk_period, slowk_matype, slowd_period, slowd_matype

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['slowk'] = slowk
    transactions_df['slowd'] = slowd
    transactions_df.dropna(inplace=True)
    return transactions_df


def stoch_slow(series: pd.Series, asset, budget, bought, fee) -> Tuple[int, int, bool]:
    if bought is False and series['slowk'] > series['slowd']:   #BUY
        bought = True
        asset = budget * (1 - fee) / series['close']
        budget = 0

    elif bought is True and series['slowk'] < series['slowd']:  # SELL
        bought = False
        budget = asset * series['close'] * (1 - fee)
        asset = 0

    return asset, budget, bought


def init_stoch_fast(df: pd.DataFrame, start: int, length: int) -> pd.DataFrame:
    high_list = csv_parser.get_nparray(df, 'high', start, length)
    low_list = csv_parser.get_nparray(df, 'low', start, length)
    close_list = csv_parser.get_nparray(df, 'close', start, length)
    fastk, fastd = talib.STOCH(high_list, low_list, close_list, 10, 6, 0)  # high, low, close, fastk_period, fastd_period, fastd_matype

    transactions_df = pd.DataFrame()
    transactions_df['close'] = df['close'].iloc[start:start + length].iloc[::-1]
    transactions_df['fastk'] = fastk
    transactions_df['fastd'] = fastd
    transactions_df.dropna(inplace=True)
    return transactions_df


def stoch_fast(series: pd.Series, asset, budget, bought, fee) -> Tuple[int, int, bool]:
    if bought is False and series['fastk'] > series['fastd']:   #BUY
        bought = True
        asset = budget * (1 - fee) / series['close']
        budget = 0

    elif bought is True and series['fastk'] < series['fastd']:  # SELL
        bought = False
        budget = asset * series['close'] * (1 - fee)
        asset = 0

    return asset, budget, bought
