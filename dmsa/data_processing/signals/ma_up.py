import pandas as pd
import talib


def calc_signal(df, fast_ma_n=5, slow_ma_n=10):
    fast_ma = talib.SMA(df["close"], timeperiod=fast_ma_n)
    slow_ma = talib.SMA(df["close"], timeperiod=slow_ma_n)

    last_df = df.shift(1)
    changes = (df["close"] - last_df["close"]) / last_df["close"]

    golden_cross = 1 * ((fast_ma > slow_ma) & (changes < 0.09))

    results = pd.DataFrame({"buy": golden_cross})

    return results
