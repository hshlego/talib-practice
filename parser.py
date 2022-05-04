import pandas as pd
import numpy as np


def get_dataframe(path="./csv_files/Binance_BTCUSDT_1h.csv") -> pd.DataFrame:
    df = pd.read_csv(path, header=1)
    return df


def get_header(df) -> str:
    return str(df.columns)


def get_all_coin_dataframe(path="./csv_files") -> list:
    coin_list = ["BTC", "ETH", "ADA", "XRP", "DOGE"]
    coin_df_list = []
    for coin in coin_list:
        file_path = path + "/Binance_" + str(coin) + "USDT_1h.csv",
        df = pd.read_csv(file_path, header=1)
        coin_df_list.append({"name": coin, "dataframe": df})

    return coin_df_list


def get_nparray(df: pd.DataFrame, column: str, start=0, length=100) -> np.ndarray:
    return np.asarray(df[column].iloc[start:start+length])
