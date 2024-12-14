from aoc_14_utils import Robot, read_input, step_robots


def compute_safety_factor(robots: list[Robot], rows: int, cols: int):

    def _sum_robots_in_range(min_x: int, max_x: int, min_y: int, max_y: int):
        return sum(1 for robot in robots if min_x <= robot.pos_x < max_x and min_y <= robot.pos_y < max_y)

     
    # Position ranges
    up = (0, rows // 2)
    down = (rows // 2 + 1, rows)
    left = (0, cols // 2)
    right = (cols // 2 + 1, cols)

    upper_left = _sum_robots_in_range(*left, *up)
    upper_right = _sum_robots_in_range(*right, *up)
    bottom_left = _sum_robots_in_range(*left, *down)
    bottom_right = _sum_robots_in_range(*right, *down)

    return upper_left * upper_right * bottom_left * bottom_right


def plot_demo(robots: list[Robot], rows: int, cols: int):
    # Plot only a small, demo environment
    if max(rows, cols) > 15:
        return

    occurrences = [
            [ 0 for _ in range(cols) ] 
            for _ in range(rows)
    ]

    for robot in robots:
        x, y = robot.pos_x, robot.pos_y
        occurrences[y][x] += 1

    for row in occurrences:
        for count in row:
            print(count or '.', end='')
        print()
    print()


def main(filename: str, rows: int, cols: int, steps: int = 100, expected: int = None):
    robots = read_input(filename)
    plot_demo(robots, rows, cols)

    step_robots(robots, rows, cols, steps)
    plot_demo(robots, rows, cols)

    result = compute_safety_factor(robots, rows, cols)

    print(f'{filename=}')
    print(f'{result=}')
    print()

    if expected is not None and result != expected:
        raise ValueError(f'Error processing {filename}: {result=}, {expected=}')


if __name__ == '__main__':
    main('aoc_14_example.txt', rows=7, cols=11, expected=12)
    main('aoc_14.txt', rows=103, cols=101)

