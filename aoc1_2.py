from collections import defaultdict
from typing import Generator

INPUT_FILE = 'aoc1_input.txt'  # Solution: 23387399

def parse_lines() -> tuple[list[int], list[int]]:
    col_1, col_2 = [], []

    with open(INPUT_FILE) as f:    
        for line in f:
            num_1, num_2 = (int(item.strip()) for item in line.split(' '*3)[:2])
            col_1.append(num_1)
            col_2.append(num_2)

    return col_1, col_2


def compute_frequency(column: list[int]) -> dict[int, int]:
    frequency = defaultdict(int)
    for num in column:
        frequency[num] += 1

    return frequency


def multiply_by_frequency(column: list[int], frequency: dict[int, int]) -> Generator[int, None, None]:
    for num in column:
        yield num * frequency[num]


def main():
    col_1, col_2 = parse_lines()
    frequency = compute_frequency(col_2)
    result = sum(multiply_by_frequency(col_1, frequency))
    print(result)


if __name__ == '__main__':
    main()
