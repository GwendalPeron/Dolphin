import APIWhisperer as AW
import Optimizer as OP
import json
import sys

def main(argv):
    api = AW.APIWhisperer()
    opt = OP.Optimizer()
    print(api.getRatios(253))

def extract_dates(quote):
    data = json.loads(quote) # potentially useless
    dates = [item["date" for item in data]
    return dates

def extract_returns(quote):
    data = json.loads(quote) # potentially useless
    returns = []
    for item in data:
        returns.append(item["return"])
    return returns

if __name__ == "__main__":
    main(sys.argv[1:])
