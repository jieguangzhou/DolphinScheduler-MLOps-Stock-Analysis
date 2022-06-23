import click
import pandas as pd

from .utils import inference


def evaluate_top_n(source_data_path, evaluate_data, api, top_n=2):
    df = pd.read_csv(source_data_path, index_col=0)
    result = inference(evaluate_data, api)
    result = pd.merge(result, df[["y"]], how="left", left_index=True, right_index=True)

    trades = {}
    for date, sub_df in result.groupby("date"):
        best_n = sub_df.sort_values("score", ascending=False)[:top_n].T.to_dict()
        trades.update(best_n)

    trades = pd.DataFrame(trades).T
    odds, pcr = calc_metrics(trades)
    odds_base, pcr_base = calc_metrics(df)
    metrics = {
        "odds": odds,
        "the profit and coss ratio": pcr,
        "odds_base": odds_base,
        "pcr_base": pcr_base,
    }
    return trades, metrics


def calc_metrics(df):
    yingkui = df["y"]
    odds = sum(yingkui > 0) / len(df)

    win_yingkui = yingkui[yingkui > 0]
    loss_yingkui = yingkui[yingkui <= 0]

    pcr = win_yingkui.mean() / -loss_yingkui.mean()
    return odds, pcr


@click.command()
@click.option("--source_data_path")
@click.option("--evaluate_data")
@click.option("--api", default="http://127.0.0.1:7000/invocations")
@click.option("--top_n", default=2, type=int)
def main(source_data_path, evaluate_data, api, top_n):
    trades, metrics = evaluate_top_n(source_data_path, evaluate_data, api, top_n)
    print(trades)
    print(metrics)


if __name__ == "__main__":
    main()
