import pandas as pd


def backtest(df: pd.DataFrame, budget: float, start: int, length: int, init_method, method) -> float:
    transactions_df = init_method(df, start, length)

    asset = 0  # 코인
    initial_budget = budget
    bought = False

    for index, row in transactions_df.iterrows():
        asset, budget, bought = method(row, asset, budget, bought)

    # 마지막에 들고 있는 돈 = 현재 종가 * 코인 량 + 현금
    end_budget = df['close'].iloc[len(transactions_df)] * asset + budget
    return end_budget / initial_budget
