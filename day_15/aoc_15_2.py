from aoc_15_utils import Grid, Step, get_step_per_move, read_input, find_cursor, compute_gps, plot


def transform_new_grid(old_grid: Grid) -> Grid:
    '''
    Adjust the grid to the new rules of part 2:
    - O is now []
    - @ is now .@
    - # is now ##
    - . is now ..
    '''
    new_grid = []

    for old_row in old_grid:
        new_row = []

        for old_cell in old_row:
            match old_cell:
                case '#':
                    new_row += [ '#', '#' ]
                case 'O':
                    new_row += [ '[', ']' ]
                case '.':
                    new_row += [ '.', '.' ]
                case '@':
                    new_row += [ '@', '.' ]
                case _:
                    raise ValueError(f'Unknown cell: {cell}')

        new_grid.append(new_row)

    return new_grid


def can_move(grid: Grid, i: int, j: int, step: Step, approvals_cache: dict[tuple[int, int], bool] = None) -> bool:
    '''
    Can I move from my current (i, j) position
    in the direction of the step?

    Now, we must do that in 2 passes on the grid:
    1. check if I can move (function can_move)
    2. actually move (function move)
    '''
    # Default value for approvals_cache
    if approvals_cache is None:
        approvals_cache = dict()

    # Avoid infinite loops
    if (i, j) in approvals_cache:
        return approvals_cache[(i, j)]

    step_i, step_j = step
    cell = grid[i][j]

    if cell == '#':
        return False

    if cell == '.':
        return True

    # Check the cell in the next direction of mine
    if not can_move(grid, i + step_i, j + step_j, step, approvals_cache):
        # I cannot move neither
        return False

    if cell != '@':
        assert cell in '[]'
        approvals_cache[(i, j)] = True

        # The box now is 2 cells wide
        # Check my sibling box too
        sibling_j = j + 1 if cell == '[' else j - 1
        if not can_move(grid, i, sibling_j, step, approvals_cache):
            return False

    return True


def move(grid: Grid, i: int, j: int, step: Step, moved: set[tuple[int, int]] = None):
    assert grid[i][j] != '#'  # We cannot move a wall

    # Default value for moved
    if moved is None:
        moved = set()

    # Avoid infinite loops
    if (i, j) in moved:
        return
    moved.add((i, j))

    # Base case: we are in an empty cell
    if grid[i][j] == '.':
        # I don't need to move
        return

    # We can move, do it!
    # First, move the cells after me in the step direction
    step_i, step_j = step
    move(grid, i + step_i, j + step_j, step, moved)

    if grid[i][j] in '[]':
        # Boxes must move their sibling too, always move in pair, since it's 2 cells wide
        sibling_j = j + 1 if grid[i][j] == '[' else j - 1
        move(grid, i, sibling_j, step, moved)

    # Do a simple move for this cell, finally
    grid[i][j], grid[i+step_i][j+step_j] = grid[i+step_i][j+step_j], grid[i][j]


def play(grid: Grid, moves: str):
    i, j = find_cursor(grid)

    for step in map(get_step_per_move, moves):
        # Now, we have 2 steps:
        # 1. Check if we can move
        # 2. Actually move
        if can_move(grid, i, j, step):
            move(grid, i, j, step)

            step_i, step_j = step
            i, j = i + step_i, j + step_j


def main(filename: str = 'aoc_15.txt', expected: int = None):
    grid, moves = read_input(filename)
    grid = transform_new_grid(grid)
    plot(grid)

    play(grid, moves)
    plot(grid)

    result = compute_gps(grid)

    print(f'{filename=}')
    print(f'{result=}')
    print()

    assert expected is None or result == expected, \
            f'Expected {expected}, got {result}'


if __name__ == '__main__':
    main('aoc_15_example_1.txt', 9021)
    main('aoc_15_example_2.txt', 618)
    main()  # 1471468 is too high
