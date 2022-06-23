import pandas as pd
import requests


def get_evaluate_data(data_path, api):
    df = pd.read_csv(data_path, index_col=0)
    data = df[df.columns.drop('label')].to_json(orient='split')
    result = requests.post(api,
                           headers={"Content-Type": 'application/json'},
                           data=data).json()
    result = pd.DataFrame(result['results'], index=df.index)
    result['score'] = result.apply(
        lambda x: x['confidence'] if x['label'] == 1 else 1 - x['confidence'], axis=1)
    result['y_pred'] = result.pop('label')

    result = pd.merge(result[['y_pred', 'score']], df[['label']],
                      how='left', left_index=True, right_index=True)

    result['tmp'] = result.index
    result['code'] = result['tmp'].apply(lambda x: x.split('$')[1])
    result['date'] = result['tmp'].apply(lambda x: x.split('$')[0])
    result.pop('tmp')

    return result


def evaluate_top_n(source_data_path, evaluate_data, api, top_n=2):
    df = pd.read_csv(source_data_path, index_col=0)
    result = get_evaluate_data(evaluate_data, api)
    result = pd.merge(result, df[['y']], how='left',
                      left_index=True, right_index=True)

    trades = {}
    for date, sub_df in result.groupby('date'):
        best_n = sub_df.sort_values('score', ascending=False)[
            :top_n].T.to_dict()
        trades.update(best_n)

    trades = pd.DataFrame(trades).T
    odds, pcr = calc_metrics(trades)
    metrics = {'odds': odds, 'the profit and coss ratio': pcr}
    return trades, metrics


def calc_metrics(df):
    yingkui = df['y']
    odds = sum(yingkui > 0) / len(df)

    win_yingkui = yingkui[yingkui > 0]
    loss_yingkui = yingkui[yingkui <= 0]

    pcr = win_yingkui.mean() / - loss_yingkui.mean()
    return odds, pcr
