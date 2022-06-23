import os

import pandas as pd
from sqlalchemy import create_engine


class CONFIG:
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_HOST = 'xxxxxxxxxxxxxxxx'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'dolphinscheduler_mlops_stock'


MYSQL_USER = CONFIG.MYSQL_USER or os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = CONFIG.MYSQL_PASSWORD or os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = CONFIG.MYSQL_HOST or os.environ.get("MYSQL_HOST")
MYSQL_PORT = CONFIG.MYSQL_PORT or os.environ.get("MYSQL_PORT")
MYSQL_DATABASE = CONFIG.MYSQL_DATABASE or os.environ.get("MYSQL_DATABASE")


def create_mysql_engine():
    mysql_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8"
    engine = create_engine(mysql_url)
    return engine


def df2sqlite(data_frame: pd.DataFrame, table_name, if_exists="replace"):
    engine = create_mysql_engine()
    print(f"save dataframe to {MYSQL_DATABASE}.{table_name}")

    data_frame.to_sql(
        table_name,
        engine,
        schema=MYSQL_DATABASE,
        if_exists=if_exists,
        index=False,
        chunksize=None,
        dtype=None,
    )
