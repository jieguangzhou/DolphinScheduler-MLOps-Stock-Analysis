import time

import pandas as pd
import requests


def inference(data_path, api):
    df = pd.read_csv(data_path, index_col=0)
    if "label" in df:
        columns = df.columns.drop("label")
    else:
        columns = df.columns
    data = df[columns].to_json(orient="split")
    while True:
        try:
            result = requests.post(
                api, headers={"Content-Type": "application/json"}, data=data
            ).json()
            break
        except:
            print("waiting model deployment start ....")
            time.sleep(3)
            continue

    result = pd.DataFrame(result["results"], index=df.index)
    result["score"] = result.apply(
        lambda x: x["confidence"] if x["label"] == 1 else 1 - x["confidence"], axis=1
    )
    result["y_pred"] = result.pop("label")

    if "label" in df:
        result = pd.merge(
            result[["y_pred", "score"]],
            df[["label"]],
            how="left",
            left_index=True,
            right_index=True,
        )

    result["tmp"] = result.index
    result["code"] = result["tmp"].apply(lambda x: x.split("$")[1])
    result["date"] = result["tmp"].apply(lambda x: x.split("$")[0])
    result.pop("tmp")

    return result
