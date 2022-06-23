import pandas as pd
from talib import abstract

__all_patterns__ = None


def get_all_patterns():
    global __all_patterns__
    if __all_patterns__:
        return __all_patterns__
    funcs = []
    for func_name in abstract.__TA_FUNCTION_NAMES__:
        func = getattr(abstract, func_name)
        group = func.info["group"]
        if group == "Pattern Recognition":
            funcs.append(func)
    __all_patterns__ = funcs
    return funcs


def calc_feature(df):
    pattern_results = {}
    for pattern in get_all_patterns():
        pattern_result = pattern(df)
        pattern_results[pattern.info["name"]] = pattern_result
    pattern_results = pd.DataFrame(pattern_results)
    return pattern_results
