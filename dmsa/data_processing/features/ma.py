from math import ceil

import pandas as pd
import talib


def calc_feature(df):
    close = df["close"]

    timeperiods = [2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233]
    delta_ratios = [0.1, 0.3, 0.4, 0.5]
    features = {}
    for timeperiod in timeperiods:
        ma = talib.SMA(close, timeperiod=timeperiod)
        relative_ma = (ma - close) / close
        for delta_ratio in delta_ratios:
            delta_n = ceil(delta_ratio * timeperiod)
            if delta_n == 0:
                continue
            features[f"delta_{delta_n}_ma_{timeperiod}"] = (
                ma - ma.shift(delta_n)
            ) / ma.shift(delta_n)
        features[f"ma_{timeperiod}"] = relative_ma
    features_df = pd.DataFrame(features)

    return features_df
