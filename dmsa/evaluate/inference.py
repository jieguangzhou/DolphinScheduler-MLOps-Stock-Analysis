import click

from dmsa.db import df2sqlite

from .utils import inference


def inference_data(evaluate_data, api, top_n=10):
    result = inference(evaluate_data, api)
    best_n = result.sort_values("score", ascending=False)[:top_n]
    df2sqlite(best_n, "candidate")
    return best_n


@click.command()
@click.option("--evaluate_data")
@click.option("--api", default="http://127.0.0.1:7000/invocations")
@click.option("--top_n", default=10, type=int)
def main(evaluate_data, api, top_n):
    trades = inference_data(evaluate_data, api, top_n)
    print(trades)


if __name__ == "__main__":
    main()
