import pandas as pd
from pytdx.hq import TdxHq_API


def get_kline(code):

    api = TdxHq_API()
    api.connect('119.147.212.81', 7709)
    try:
        if code.startswith('sh'):
            market = 1
        else:
            market = 0
        code = code.replace('.', '')
        code = code[2:]
        data = api.get_security_bars(category=7,
                                     market=market,
                                     code=code,
                                     start=0,
                                     count=300)
        df = api.to_df(data)
    finally:
        api.disconnect()

    df['datetime'] = pd.to_datetime(df.pop('datetime'))
    df = df.sort_values('datetime')
    df['volume'] = df.pop('vol')
    df = df.drop(['amount', 'year', 'month', 'day', 'hour', 'minute'], axis=1)

    return df
