import pandas as pd
import talib


def calc_feature(df):
    close = df["close"]
    upperband, middleband, lowerband = talib.BBANDS(
        close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
    )

    features = {}

    features["upperband_distance"] = (close - upperband) / upperband
    features["middleband_distance"] = (close - middleband) / middleband
    features["lowerband_distance"] = (close - lowerband) / lowerband

    features_df = pd.DataFrame(features)

    return features_df
