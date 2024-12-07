from aoc_07_utils import Operator, read_input, sum_valid_results


MUL: Operator = lambda x, y: x * y
ADD: Operator = lambda x, y: x + y


def main():
    inputs = read_input()
    result = sum_valid_results(inputs, all_operators=[MUL, ADD])
    print(result)


if __name__ == '__main__':
    main()




