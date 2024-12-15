from aoc_15_utils import Grid, Step, get_step_per_move, read_input, find_cursor, compute_gps, plot


def move(grid: Grid, i: int, j: int, step: Step) -> bool:
    '''
    Can I move from my current (i, j) position
    in the direction of the step?
    '''
    step_i, step_j = step
    cell = grid[i][j]

    if cell == '#':
        return False

    if cell == '.':
        return True

    if not move(grid, i + step_i, j + step_j, step):
        # The next ball cannot move, so can't I
        return False

    # We can move, do it!
    grid[i][j], grid[i+step_i][j+step_j] = grid[i+step_i][j+step_j], grid[i][j]

    return True


def play(grid: Grid, moves: str):
    i, j = find_cursor(grid)

    for step in map(get_step_per_move, moves):
        if move(grid, i, j, step):
            step_i, step_j = step
            i, j = i + step_i, j + step_j


def main(filename: str = 'aoc_15.txt', expected: int = None):
    grid, moves = read_input(filename)
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
    main('aoc_15_example_0.txt', 2028)
    main('aoc_15_example_1.txt', 10092)
    main()
