import importlib

import click

from dmsa.db import df2sqlite

from .utils import calc_batch_data, load_names


def calc_feature(data_path, feature_name):
    try:
        func = importlib.import_module(
            f"dmsa.data_processing.features.{feature_name}"
        ).calc_feature
    except Exception as e:
        print(e)
        print(f"feature {feature_name} does not exist")
        return None
    df = calc_batch_data(data_path, func, feature_name)
    table_name = f"feature_{feature_name}"
    df2sqlite(df, table_name)
    return df


def calc_features(data_path, feature_name_file):

    feature_names, _ = load_names(feature_name_file)

    print(feature_names)

    for feature_name in feature_names:
        calc_feature(data_path, feature_name)


@click.command()
@click.option("--data_path",)
@click.option("--name_file", default=None)
@click.option("--name", default=None)
def main(data_path, name_file, name):
    if name_file is not None:
        calc_features(data_path, name_file)
    elif name is not None:
        calc_feature(data_path, name)

    else:
        raise Exception(
            "At least one of feature_name_file and feature_name is not null"
        )


if __name__ == "__main__":
    main()
