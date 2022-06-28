import os

import click
import pandas as pd
from tqdm import tqdm

from dmsa.db import create_mysql_engine

from .utils import load_names


def concat(datas_g):
    datas = []
    for d_g in datas_g:
        datas.append(d_g)
    datas = pd.concat(datas)
    return datas


def load_signals(signal_name):
    engine = create_mysql_engine()
    signals = pd.read_sql(
        f"SELECT code, date FROM signal_{signal_name} WHERE buy=1", con=engine, chunksize=50000,
    )
    signals = concat(signals)
    return signals


def load_features(feature_name):
    engine = create_mysql_engine()
    features = pd.read_sql(
        f"SELECT * FROM feature_{feature_name}", con=engine, chunksize=50000)
    features = concat(features)
    return features


def load_signal_feature(signal_name, feature_name):
    sql_query = f"SELECT * FROM signal_{signal_name} a LEFT JOIN feature_{feature_name} b ON a.code = b.code AND a.date = b.date WHERE a.buy=1;"
    print(sql_query)
    datas = pd.read_sql(sql_query, con=create_mysql_engine())
    datas = concat(datas)
    return datas


def create_datas(feature_signal_file):
    feature_names, signal_names = load_names(feature_signal_file)
    assert len(signal_names) == 1, f"Only Support 1 signal, but get {signals}"
    signal_name = signal_names[0]
    signals = load_signals(signal_name)
    datas = signals
    for feature_name in tqdm(feature_names, desc="load features"):
        features = load_features(feature_name)
        datas = pd.merge(datas, features, how="left", on=["code", "date"])

    return datas


def set_labels(signals, data_path, next_n=1):
    new_signals = []
    for code, sub_signal_df in signals.groupby("code"):
        path = os.path.join(data_path, f"{code}.csv")
        data_df = pd.read_csv(path)
        next_n_df = data_df.shift(-next_n)
        data_df["y"] = (next_n_df["close"] -
                        data_df["close"]) / data_df["close"]

        data_df = data_df[~data_df["y"].isna()]
        data_df["label"] = (data_df["y"] > 0) * 1

        sub_signal_df = pd.merge(
            sub_signal_df, data_df[["label", "date", "y"]], how="left", on=["date"]
        )
        sub_signal_df["code"] = code
        new_signals.append(sub_signal_df)

    new_signals = pd.concat(new_signals)
    return new_signals


def set_dataset_index(dataset):
    dataset.index = dataset.apply(
        lambda x: x["date"] + "$" + x["code"], axis=1)
    dataset.pop("date")
    dataset.pop("code")


def get_inference_datas(feature_signal_file, save_path):
    datas = create_datas(feature_signal_file)
    date = sorted(set(datas["date"]))[-1]
    datas = datas[datas["date"] == date]
    set_dataset_index(datas)

    datas.to_csv(os.path.join(save_path), index=True)
    print(f"save data to {save_path}")
    print(f"datas : {len(datas)}")


def get_training_data(feature_signal_file, data_path, save_path, test_date_n=7):
    datas = create_datas(feature_signal_file)
    datas = set_labels(datas, data_path)

    datas = datas[~datas["label"].isna()]
    datas["label"] = datas["label"].astype(int)

    dates = sorted(set(datas["date"]))
    dates = dates[-121:]
    datas = datas.sort_values("date")

    train_dates = dates[:-test_date_n]
    test_dates = dates[-test_date_n:]
    model_datas = datas[datas.columns.drop("y")]

    train_dataset = model_datas[model_datas["date"].isin(train_dates)]
    test_dataset = model_datas[model_datas["date"].isin(test_dates)]
    set_dataset_index(train_dataset)
    set_dataset_index(test_dataset)

    os.makedirs(save_path, exist_ok=True)
    print(f"save data to {save_path}")
    print(f"train_dataset : {len(train_dataset)}")
    print(f"test_dataset : {len(test_dataset)}")

    train_dataset.to_csv(os.path.join(save_path, "train.csv"), index=True)
    test_dataset.to_csv(os.path.join(save_path, "test.csv"), index=True)

    set_dataset_index(datas)
    datas.to_csv(os.path.join(save_path, "source.csv"), index=True)

    return train_dataset, test_dataset


@click.command()
@click.option("--task_type")
@click.option("--config", type=str)
@click.option("--save_path", type=str)
@click.option("--data_path", default=None)
def main(task_type, config, data_path, save_path):
    if task_type == "train":
        get_training_data(config, data_path, save_path)

    elif task_type == "inference":
        get_inference_datas(config, save_path)

    else:
        raise Exception("only support train and inference")


if __name__ == "__main__":
    main()
