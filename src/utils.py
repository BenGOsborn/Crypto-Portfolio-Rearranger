from binance import Client
import pandas as pd
import numpy as np
from datetime import datetime
import itertools


class DataClass:
    def __init__(self, api_key: str, api_secret: str, default_pair: str = "USDT"):
        self.__client = Client(api_key, api_secret)
        self.__default_pair = default_pair

    # Get all tickers
    def get_pairs(self):
        raw_tickers = self.__client.get_all_tickers()
        tickers = []
        for ticker in raw_tickers:
            if ticker["symbol"].endswith(self.__default_pair) and not ticker["symbol"].startswith(self.__default_pair) and not "DOWN" in ticker["symbol"] and not "UP" in ticker["symbol"]:
                tickers.append(ticker["symbol"])

        return tickers

    # Make a dataframe of the trading pair every hour over the specified number of days
    def get_data(self, pair: str, days: int):
        data = self.__client.get_historical_klines(
            pair, self.__client.KLINE_INTERVAL_1HOUR, f"{days} day ago UTC")
        cols = ["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume",
                "num_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"]
        df = pd.DataFrame(data, columns=cols)
        df = df.iloc[:, 0:5]
        df["open_time"] = pd.to_datetime((pd.to_numeric(
            df["open_time"]) / 1000).apply(lambda x: datetime.fromtimestamp(x)))
        df.set_index("open_time", inplace=True)
        df["open"], df["high"], df["low"], df["close"] = pd.to_numeric(df["open"]), pd.to_numeric(
            df["high"]), pd.to_numeric(df["low"]), pd.to_numeric(df["close"])

        return df


class Utils:
    # Return the price percent changes correlation coefficient
    @staticmethod
    def correlation(df1: pd.DateOffset, df2: pd.DataFrame):
        close1 = df1["close"].pct_change().rolling(12).mean().dropna()
        close2 = df2["close"].pct_change().rolling(12).mean().dropna()
        corr = np.corrcoef(close1.values[1:], close2.values[1:])[0, 1]
        if corr == np.nan:
            raise Exception("Returned NaN")
        return corr

    # Rank token pairs based on the most correlated or inversely correlated
    @staticmethod
    def get_correlations(data: DataClass, days: int, limit: int = None, inverse: bool = True):
        pairs = data.get_pairs()
        if limit != None:
            pairs = pairs[:limit]
            np.random.shuffle(pairs)

        correlations = []
        for pair in itertools.combinations(pairs, 2):
            try:
                data1 = data.get_data(pair[0], days)
                data2 = data.get_data(pair[1], days)
                corr = Utils.correlation(data1, data2)
                correlations.append((pair[0], pair[1], corr))
            except Exception as e:
                print(f"Encountered exception '{e}' for pair '{pair}'")

        sorted_correlations = sorted(
            correlations, key=lambda x: x[2], reverse=not inverse)
        return sorted_correlations
