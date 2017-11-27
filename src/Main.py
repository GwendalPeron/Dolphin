import APIWhisperer as AW
import Optimizer as OP
import sys

def main(argv):
    api = AW.APIWhisperer()
    opt = OP.Optimizer()
    print(api.getRatios(253))

if __name__ == "__main__":
    main(sys.argv[1:])
