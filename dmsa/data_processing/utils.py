import os

import pandas as pd
from tqdm import tqdm

DATA_FOLDER = "data"


def load_all_datas(data_path=DATA_FOLDER):
    print(f"load data from data path: {data_path}")
    dfs = []
    for file in os.listdir(data_path):
        path = os.path.join(data_path, file)
        code = file.replace(".csv", "")
        df = pd.read_csv(path, index_col=0)
        df["code"] = code
        dfs.append(df)
    return dfs


def calc_batch_data(data_path, func, name):
    datas = load_all_datas(data_path)
    strategy_dfs = []
    for df in tqdm(datas, desc=f"run {name}"):
        result = func(df)
        result["code"] = df["code"]
        result["date"] = df.index
        strategy_dfs.append(result)
    strategy_dfs = pd.concat(strategy_dfs).reset_index(drop=True)
    return strategy_dfs


def load_names(file):
    features = []
    signals = []
    with open(file) as r_f:
        for line in r_f:
            if line.startswith("feature:"):
                features.append(line.replace("feature:", "").strip())
            elif line.startswith("signal:"):
                signals.append(line.replace("signal:", "").strip())

    return features, signals
