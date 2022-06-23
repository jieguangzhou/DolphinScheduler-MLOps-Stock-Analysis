import pandas as pd
import talib


def calc_signal(df, fast_ma_n=5, slow_ma_n=10):
    fast_ma = talib.SMA(df["close"], timeperiod=fast_ma_n)
    slow_ma = talib.SMA(df["close"], timeperiod=slow_ma_n)

    fast_ma_last_day = fast_ma.shift(1)
    slow_ma_last_day = slow_ma.shift(1)

    golden_cross = 1 * ((fast_ma > slow_ma) & (fast_ma_last_day <= slow_ma_last_day))

    results = pd.DataFrame({"buy": golden_cross})

    return results
