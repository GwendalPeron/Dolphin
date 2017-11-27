import APIWhisperer as AW
import Optimizer as OP
import numpy as np
import pandas as pd
import json
import sys

def main(argv):
    api = AW.APIWhisperer()
    opt = OP.Optimizer()
    print(api.getRatios(253))

def extract_dates(quote):
    data = json.loads(quote) # potentially useless
    dates = [item["date"] for item in data]
    return dates

def extract_returns(quote):
    data = json.loads(quote) # potentially useless
    returns = []
    for item in data:
        returns.append(item["return"])
    return returns

def prep_data(assetids):
    assets = assetids
    dates = [] # TODO get dates from first quote
    data = []
    for id in assetids:
        quote = "{}" # TODO get quote from APIWhisperer
        rets = extract_returns(quote)
        data.append(rets)
    data = np.array(data)

    returns = pd.DataFrame(data, columns=assets, index=dates)
    avg_rets = returns.mean()
    cov_mat = returns.cov()

    return returns, cov_mat, avg_rets


if __name__ == "__main__":
    main(sys.argv[1:])
