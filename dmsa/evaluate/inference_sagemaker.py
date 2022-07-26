import os
from tempfile import TemporaryDirectory

import click
import pandas as pd

from dmsa.data_api.s3_api import download_data_without_bucket
from dmsa.db import df2sqlite


def inference_data(evaluate_data, top_n=10):
    with TemporaryDirectory() as folder_path:
        df_path = os.path.join(folder_path, "df.csv")
        download_data_without_bucket(evaluate_data, df_path)
        df = pd.read_csv(df_path, index_col=0)

    result = df.sort_values("prediction", ascending=False)[:top_n]
    result = result[["prediction"]]
    result["score"] = result.pop("prediction")
    result["confidence"] = result.pop("score")

    result["tmp"] = result.index
    result["code"] = result["tmp"].apply(lambda x: x.split("$")[1])
    result["date"] = result["tmp"].apply(lambda x: x.split("$")[0])
    result.pop("tmp")
    df2sqlite(result, "candidate_sagemaker")
    return result


@click.command()
@click.option("--evaluate_data")
@click.option("--top_n", default=10, type=int)
def main(evaluate_data, top_n):
    trades = inference_data(evaluate_data, top_n)
    print(trades)


if __name__ == "__main__":
    main()
