import pandas as pd
import numpy as np


# default : 비트코인 1h 파일을 불러옴
def get_dataframe(path="./csv_files/Binance_BTCUSDT_1h.csv") -> pd.DataFrame:
    df = pd.read_csv(path, header=1)
    return df


# 코인 5개의 데이터프레임을 리스트 형태로 반환
def get_all_coin_dataframe(path="./csv_files") -> list:
    coin_list = ["BTC", "ETH", "ADA", "XRP", "DOGE"]
    coin_df_list = []
    for coin in coin_list:
        file_path = path + "/Binance_" + str(coin) + "USDT_1h.csv",
        df = pd.read_csv(file_path, header=1)
        coin_df_list.append({"name": coin, "dataframe": df})

    return coin_df_list


# 데이터프레임 헤더값
def get_header(df) -> str:
    return str(df.columns)


# 데이터프레임의 특정 column 값을 범위 만큼 반환, row 역순
def get_nparray(df: pd.DataFrame, column: str, start=0, length=100) -> np.ndarray:
    temp_df = df[column].iloc[start:start+length]
    return np.asarray(temp_df[::-1])
