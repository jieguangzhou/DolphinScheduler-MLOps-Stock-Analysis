import akshare as ak


def get_spot_datas():
    source_spot_data = ak.stock_zh_a_spot_em()
    source_spot_data["code"] = source_spot_data["代码"].apply(
        lambda x: "sh." + x if x.startswith("6") else "sz." + x
    )

    spot_datas = source_spot_data[["code", "名称", "涨跌幅", "涨速", "5分钟涨跌"]]
    return spot_datas
