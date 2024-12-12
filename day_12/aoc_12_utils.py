from typing import TypeAlias, Generator

Matrix: TypeAlias = list[str]

Coordinate: TypeAlias = tuple[int, int]  # i, j

Region: TypeAlias = set[Coordinate]


def read_input(filename: str = 'aoc_12.txt') -> Matrix:
    with open(filename) as f:
        return [line.strip() for line in f]


def safe_matrix_get(plot: Matrix, i: int, j: int) -> bool:
    is_valid = i >= 0 and j >= 0 and i < len(plot) and j < len(plot[i])
    return plot[i][j] if is_valid else '.'


def find_regions(plot: Matrix) -> Generator[Region, None, None]:
    visited: Region = set()

    for i, row in enumerate(plot):
        for j, cell in enumerate(row):
            if (i, j) in visited:
                continue

            yield expand_region(plot, i, j, visited)


def expand_region(plot: Matrix, i: int, j: int, visited: Region, partial_result: Region = None) -> Region:
    # Default arguments
    if partial_result is None:
        partial_result = set()

    partial_result.add((i, j))
    visited.add((i, j))

    for diff_i, diff_j in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        next_i, next_j = i + diff_i, j + diff_j
        my_symbol = plot[i][j]
        neighbour_symbol = safe_matrix_get(plot, next_i, next_j)
        if my_symbol == neighbour_symbol and (next_i, next_j) not in visited:
            # Expand the region in that direction
            expand_region(plot, next_i, next_j, visited, partial_result)

    return partial_result


def compute_area(region: Region) -> int:
    return len(region)
