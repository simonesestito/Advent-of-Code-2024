from collections import defaultdict
from typing import Generator

INPUT_FILE = 'aoc1_input.txt'  # Solution: 1197984

def parse_lines() -> tuple[list[int], list[int]]:
    col_1, col_2 = [], []

    with open(INPUT_FILE) as f:    
        for line in f:
            num_1, num_2 = (int(item.strip()) for item in line.split(' '*3)[:2])
            col_1.append(num_1)
            col_2.append(num_2)

    col_1.sort()
    col_2.sort()

    return col_1, col_2


def compute_distance_in_pair(col_1: list[int], col_2: list[int]) -> Generator[int, None, None]:
    for num_1, num_2 in zip(col_1, col_2):
        yield abs(num_1 - num_2)

def main():
    col_1, col_2 = parse_lines()
    distances = sum(compute_distance_in_pair(col_1, col_2))
    print(distances)


if __name__ == '__main__':
    main()
