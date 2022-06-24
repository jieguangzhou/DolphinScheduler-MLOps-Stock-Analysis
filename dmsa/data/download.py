import os
import sys

from tqdm import tqdm

from dmsa.data_api.china_daily_data import download_stock, get_stock_pool


def download_all_stocks(start_date=None, end_date=None, save_folder="data", n=None):
    codes = list(get_stock_pool())
    os.makedirs(save_folder, exist_ok=True)
    if n:
        codes = codes[:n]
    for code in tqdm(codes):
        download_stock(code, save_folder, start_date, end_date)


if __name__ == "__main__":
    save_folder = sys.argv[1]
    download_all_stocks(start_date="2021-01-01", save_folder=save_folder)
    print(os.path.abspath(save_folder))
