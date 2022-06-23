import pandas as pd
import talib


def calc_feature(df):
    close = df["close"]

    timeperiods = [2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    features = {}
    for timeperiod in timeperiods:
        ma = talib.SMA(close, timeperiod=timeperiod)
        relative_ma = (ma - close) / close
        features[f"ma_{timeperiod}"] = relative_ma
    features_df = pd.DataFrame(features)

    return features_df
