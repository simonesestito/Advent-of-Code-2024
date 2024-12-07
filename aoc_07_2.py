from aoc_07_utils import Operator, read_input, sum_valid_results
from math import ceil, log10


MUL = lambda x, y: x * y
ADD = lambda x, y: x + y


def digits_of(n: int) -> int:
    return max(1, int(ceil(log10(n + 1e-4))))

CON = lambda x, y: x * 10 ** digits_of(y) + y


def main():
    inputs = read_input()
    result = sum_valid_results(inputs, all_operators=[CON, MUL, ADD])
    print(result)


if __name__ == '__main__':
    main()




