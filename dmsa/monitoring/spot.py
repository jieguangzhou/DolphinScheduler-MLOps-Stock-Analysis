from dmsa.data_api.china_spot import get_spot_datas
from dmsa.db import df2sqlite


def monitoring_spot():
    spot_datas = get_spot_datas()
    df2sqlite(spot_datas, "spot")


if __name__ == "__main__":
    monitoring_spot()
