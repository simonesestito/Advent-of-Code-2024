from typing import TypeAlias, NamedTuple

Maze: TypeAlias = list[list[str]]

Direction: TypeAlias = tuple[int, int]

Coordinate: TypeAlias = tuple[int, int]


def read_input(filename: str) -> Maze:
    with open(filename) as f:
        return [ list(line.strip()) for line in f ]


def find_maze_cell(maze: Maze, expected: str) -> tuple[int, int]:
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == expected:
                return i, j
