from typing import TypeAlias
import heapq

Grid: TypeAlias = list[list[str]]

Coordinate: TypeAlias = tuple[int, int]  # i, j

Route: TypeAlias = tuple[int, int, int]  # score, i, j


def read_input(filename: str) -> Grid:
    lines = []

    with open(filename) as f:
        # Read the first 1024 lines, or until EOF
        for _ in range(1024):
            line = f.readline()
            if not line:
                break  # EOF

            line = line.strip()
            x, y = map(int, line.split(','))
            lines.append((x, y))

    assert len(lines) <= 1024

    # Compute the grid
    grid: Grid = [ [ '.' for _ in range(71) ] for _ in range(71) ]
    for x, y in lines:
        grid[y][x] = '#'

    return grid



def safe_grid_get(grid: Grid, i: int, j: int) -> str:
    if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        return grid[i][j]

    # Out of bounds: default to a wall
    return '#'


def solve_grid(grid: Grid) -> int:
    best_routes: list[Route] = [(0,0,0)]
    visited: set[Coordinate] = set()

    while best_routes:
        # Pop the best route so far
        score, i, j = heapq.heappop(best_routes)
        if (i, j) in visited:
            continue
        visited.add((i, j))

        # Base case: the end cell
        if i == 70 and j == 70:
            return score

        # Where can we go?
        dirs = [ (0,1), (0,-1), (1,0), (-1,0) ]
        for dir_i, dir_j in dirs:
            next_i, next_j = i + dir_i, j + dir_j
            next_cell = safe_grid_get(grid, next_i, next_j)
            if next_cell == '.':
                # Go there!
                heapq.heappush(best_routes, (score + 1, next_i, next_j))

    return None


def main(filename: str = 'aoc_18.txt'):
    grid = read_input(filename)
    result = solve_grid(grid)
    print(result)


if __name__ == '__main__':
    main()

