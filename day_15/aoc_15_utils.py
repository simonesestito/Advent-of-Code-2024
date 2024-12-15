from typing import TypeAlias

Grid: TypeAlias = list[list[str]]

Step: TypeAlias = tuple[int, int]


def read_input(filename: str) -> tuple[Grid, str]:
    with open(filename) as f:
        # First, there are the lines of the grid
        grid: Grid = []
        while line := f.readline().strip():
            grid.append(list(line))

        # Then, read the moves
        moves = []
        while line := f.readline():
            moves.append(line.strip())
        moves = ''.join(moves)

    return grid, moves


def get_step_per_move(move: str) -> Step:
    match move:
        case '^':
            return (-1, 0)
        case 'v':
            return (1, 0)
        case '<':
            return (0, -1)
        case '>':
            return (0, 1)
        case _:
            raise ValueError(f'Unknown move: {move}')


def find_cursor(grid: Grid, cursor: str = '@') -> tuple[int, int]:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == cursor:
                return i, j


def compute_gps(grid: Grid) -> int:
    gps: int = 0

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'O' or cell == '[':
                # Add the GPS of this box to the final score
                # Part 1 uses O, part 2 uses [
                gps += 100 * i + j

    return gps


def plot(grid: Grid):
    if len(grid) >= 30:
        return
        
    for row in grid:
        print(''.join(row))
    print()
