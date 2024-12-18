from typing import TypeAlias
import heapq

Grid: TypeAlias = list[list[str]]

Coordinate: TypeAlias = tuple[int, int]  # i, j

Route: TypeAlias = tuple[int, int, int, Coordinate]  # score, i, j, prev


def read_input(filename: str) -> tuple[Grid, list[Coordinate]]:
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


        # Keep reading all next lines in the file
        lines = []
        while line := f.readline():
            line = line.strip()
            x, y = map(int, line.split(','))
            lines.append((y, x))

    return grid, lines



def safe_grid_get(grid: Grid, i: int, j: int) -> str:
    if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        return grid[i][j]

    # Out of bounds: default to a wall
    return '#'


def solve_grid(grid: Grid) -> int:
    best_routes: list[Route] = [(0,0,0,None)]
    visited: dict[Coordinate, Coordinate] = dict()

    while best_routes:
        # Pop the best route so far
        score, i, j, prev = heapq.heappop(best_routes)
        if (i, j) in visited:
            continue
        visited[(i, j)] = prev

        assert grid[i][j] == '.'

        # Base case: the end cell
        if i == 70 and j == 70:
            break

        # Where can we go?
        dirs = [ (0,1), (0,-1), (1,0), (-1,0) ]
        for dir_i, dir_j in dirs:
            next_i, next_j = i + dir_i, j + dir_j
            next_cell = safe_grid_get(grid, next_i, next_j)
            if next_cell == '.':
                # Go there!
                heapq.heappush(best_routes, (score + 1, next_i, next_j, (i, j)))

    if (70, 70) not in visited:
        return None

    all_prevs = { (70, 70) }
    prev = visited[(70, 70)]
    while prev is not None:
        all_prevs.add(prev)
        prev = visited[prev]
    return all_prevs


def solve_new_blocks(grid: Grid, new_blocks: list[Coordinate]) -> Coordinate:
    path = solve_grid(grid)
    for i, j in new_blocks:
        grid[i][j] = '#'
        if (i, j) in path:
            # Recompute
            path = solve_grid(grid)
            if not path:
                return i, j


def main(filename: str = 'aoc_18.txt'):
    grid, new_blocks = read_input(filename)
    y, x = solve_new_blocks(grid, new_blocks)
    print(f'{x},{y}')


if __name__ == '__main__':
    main()

