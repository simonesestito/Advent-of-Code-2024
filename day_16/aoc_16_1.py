from aoc_16_utils import Maze, read_input, find_maze_cell
from maze_heap import MazeHeap
from maze_state import MazeState


def solve_maze(maze: Maze) -> int:
    '''
    Solve the maze, finding the score of the minimum path
    from S to E, using a min heap
    '''
    start_i, start_j = find_maze_cell(maze, 'S')

    # Begin navigating the maze from the start cell, facing right
    i, j, direction, score = start_i, start_j, (0, 1), 0

    # Use an heap to save the best routes
    best_routes: MazeHeap = MazeHeap(maze)
    best_routes.push(MazeState(i, j, direction, score))

    while best_routes:
        # Pop the best route from the heap
        best_state = best_routes.pop()
        i, j, direction, score = best_state.i, best_state.j, best_state.direction, best_state.score
        dir_i, dir_j = direction

        # Base case: we reached the end cell
        if maze[i][j] == 'E':
            return score

        # Go straight
        straight_i, straight_j, straight_score = i + dir_i, j + dir_j, score + 1
        best_routes.push(MazeState(straight_i, straight_j, direction, straight_score))

        # Turn left and walk 1 step
        left_dir = (-dir_j, dir_i)
        left_i, left_j, left_score = i + left_dir[0], j + left_dir[1], score + 1000 + 1
        best_routes.push(MazeState(left_i, left_j, left_dir, left_score))

        # Turn right and walk 1 step
        right_dir = (dir_j, -dir_i)
        right_i, right_j, right_score = i + right_dir[0], j + right_dir[1], score + 1000 + 1
        best_routes.push(MazeState(right_i, right_j, right_dir, right_score))


def main(filename: str = 'aoc_16.txt', expected: int = None):
    maze = read_input(filename)
    result = solve_maze(maze)

    print(f'{filename=}')
    print(f'{result=}')
    print()

    assert expected is None or expected == result, \
            f'Expected {expected}, got {result}'


if __name__ == '__main__':
    main('aoc_16_example_0.txt', 7036)
    main('aoc_16_example_1.txt', 11048)
    main()
