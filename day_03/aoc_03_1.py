import re
from typing import Generator


def read_input(filename: str = 'aoc_03.txt') -> str:
    with open(filename, 'r') as file:
        return file.read()


def find_mul(input_str: str) -> Generator[int, None, None]:
    for match in re.findall(r'mul\(\d{1,3},\d{1,3}\)', input_str):
        # Extract the two numbers from the match
        a, b = map(int, match[4:-1].split(','))
        yield a * b


def main():
    input_str = read_input()
    result = sum(find_mul(input_str))
    print(result)


if __name__ == '__main__':
    main()