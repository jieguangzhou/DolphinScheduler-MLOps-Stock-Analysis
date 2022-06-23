import pandas as pd
import talib


def calc_signal(df, fast_ma_n=5, slow_ma_n=10):
    fast_ma = talib.SMA(df["close"], timeperiod=fast_ma_n)
    slow_ma = talib.SMA(df["close"], timeperiod=slow_ma_n)

    golden_cross = 1 * (fast_ma > slow_ma)

    results = pd.DataFrame({"buy": golden_cross})

    return results
