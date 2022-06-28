import pandas as pd

from dmsa.data_api.china_timekline import get_kline
from dmsa.db import create_mysql_engine, df2sqlite


def get_all_codes():
    df = pd.read_sql("SELECT code from candidate;", con=create_mysql_engine())
    codes = list(df['code'])
    return codes


def monitoring_kline():
    codes = get_all_codes()
    dfs = []
    for code in codes:
        df = get_kline(code)
        df['code'] = code

        dates = sorted({dt.date() for dt in df['datetime']})

        today = dates[-1]
        previous_day = dates[-2]

        today_df = df[df['datetime'].apply(lambda x:x.date() == today)].copy()
        previous_day_df = df[df['datetime'].apply(
            lambda x:x.date() == previous_day)]

        last_close = previous_day_df.iloc[-1].close
        today_df['changes'] = 100 * \
            (today_df['close'] - last_close) / last_close

        dfs.append(today_df)

    total_df = pd.concat(dfs)
    datas = []
    for time, sub_df in total_df.groupby('datetime'):
        mean_changes = sub_df['changes'].mean()
        datas.append({
            'code': 'candidate',
            'time': time,
            'changes': mean_changes
        })
    df = pd.DataFrame(datas)
    total_df = pd.concat([total_df, df])

    df2sqlite(total_df, "kline")


if __name__ == "__main__":
    monitoring_kline()
