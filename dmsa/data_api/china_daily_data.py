import os
import re
import sys

import baostock as bs
import pandas as pd
from tqdm import tqdm

RE_CODE_NUM = re.compile("\d+")

lg = bs.login()


def deal_time(time_string):
    time_string = time_string[:12]
    date = "-".join([time_string[:4], time_string[4:6], time_string[6:8]])
    hm = ":".join([time_string[8:10], time_string[10:12]])
    findall_time = "{} {}".format(date, hm)
    return findall_time


def get_daily_data(code, start_date, end_date):
    rs = bs.query_history_k_data_plus(
        code,
        "date,open,high,low,close,volume",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="2",
    )
    df = parse_result(rs, set_date2index=True, to_float=True)
    return df


def parse_result(rs, set_date2index=False, set_time2index=False, to_float=False):
    data_list = []
    while (rs.error_code == "0") & rs.next():
        data_list.append(rs.get_row_data())
    df = pd.DataFrame(data_list, columns=rs.fields)
    if len(df) == 0:
        raise Exception(rs.error_msg)
    if set_date2index:
        df.index = df.pop("date")
    if set_time2index:
        times = df.pop("time")
        times = [deal_time(t) for t in times]
        df.index = times
        df.pop("date")
    if to_float:
        df = df.astype(float).round(3)
    return df


def get_zhongzheng500(day=None, only_code=False):
    rs = bs.query_zz500_stocks()
    df = parse_result(rs)
    if only_code:
        return list(df["code"])
    df["base_code"] = df["code"].apply(lambda x: RE_CODE_NUM.findall(x)[0])
    return df


def get_stock_pool():

    rs = bs.query_stock_basic()
    all_stocks = parse_result(rs)

    all_stocks[~all_stocks["outDate"].apply(lambda x: bool(x.strip()))]
    all_stocks = all_stocks[all_stocks["type"] == "1"]
    codes = set(all_stocks["code"])
    return codes


def download_stock(code, save_folder, start_date=None, end_date=None):

    start_date = start_date or "2020-01-01"
    try:
        df = get_daily_data(code, start_date, end_date)
    except Exception:
        print("download {} {}-{} error".format(code, start_date, end_date,))
        return 0
    file_name = os.path.join(save_folder, "{}.csv".format(code))
    df.to_csv(file_name)
    return df
