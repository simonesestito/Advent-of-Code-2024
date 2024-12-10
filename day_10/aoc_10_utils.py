from typing import TypeAlias, Generator

Point: TypeAlias = tuple[int, int]

Matrix: TypeAlias = list[list[int]]


def read_input(filename: str = 'aoc_10.txt') -> Matrix:
    with open(filename) as f:
        return [
            [ int(cell) for cell in line.strip() ]
            for line in f
        ]


def find_trailheads(matrix: Matrix) -> Generator[Point, None, None]:
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == 0:
                yield i, j
