import importlib

import click

from dmsa.db import df2sqlite

from .utils import calc_batch_data, load_names


def calc_signal(data_path, signal_name):
    try:
        func = importlib.import_module(
            f"dmsa.data_processing.signals.{signal_name}"
        ).calc_signal
    except Exception as e:
        print(f"signal {signal_name} does not exist")
        return None
    df = calc_batch_data(data_path, func, signal_name)
    table_name = f"signal_{signal_name}"
    df2sqlite(df, table_name)
    return df


def calc_signals(data_path, signal_name_file):

    _, signal_names = load_names(signal_name_file)

    print(signal_names)

    for signal_name in signal_names:
        calc_signal(data_path, signal_name)


@click.command()
@click.option("--data_path")
@click.option("--name_file", default=None)
@click.option("--name", default=None)
def main(data_path, name_file, name):
    if name_file is not None:
        calc_signals(data_path, name_file)
    elif name is not None:
        calc_signal(data_path, name)

    else:
        raise Exception("At least one of signal_name_file and signal_name is not null")


if __name__ == "__main__":
    main()
