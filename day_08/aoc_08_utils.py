'''
Common utility functions for both parts of Day 8
'''
from typing import TypeAlias, Generator
from collections import defaultdict


Coordinate: TypeAlias = tuple[int, int]

FrequenciesTable: TypeAlias = dict[str, list[Coordinate]]

MapSize: TypeAlias = tuple[int, int]


def read_input(filename: str = 'aoc_08.txt') -> tuple[FrequenciesTable, MapSize]:
    freqs: FrequenciesTable = defaultdict(list)

    rows, cols = 0, 0

    with open(filename) as f:
        for i, line in enumerate(f):
            rows += 1  # Count rows

            for j, cell in enumerate(line.strip()):
                if i == 0:
                    cols += 1  # Count columns

                if cell != '.':
                    freqs[cell].append((i, j))

    return freqs, (rows, cols)


def iter_pairs(items: list[Coordinate]) -> Generator[Coordinate, None, None]:
    for i, first in enumerate(items):
        for second in items[i+1:]:
            yield first, second

def within_matrix_area(size: MapSize, coordinate: Coordinate) -> bool:
    map_rows, map_cols = size
    i, j = coordinate
    return 0 <= j < map_rows and 0 <= i < map_cols

