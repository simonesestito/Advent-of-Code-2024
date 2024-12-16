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
    best_routes.push(MazeState(i, j, direction, score), from_state=None)

    # Keep track of the best score to reach the end cell, as soon as we find it
    best_end_state: int | None = None

    while best_routes:
        # Pop the best route from the heap
        best_state = best_routes.pop()
        i, j, direction, score, _ = best_state
        dir_i, dir_j = direction        

        # Stop if we are considering a path with a score higher than the best path's score
        if best_end_state is not None and score > best_end_state.score:
            break

        # Base case: we reached the end cell
        if maze[i][j] == 'E':
            # Since we want ALL best paths, save the score and continue.
            # We will stop later, when the best path popped from the heap has a higher score.
            best_end_state = best_state
            continue

        # Go straight
        straight_i, straight_j, straight_score = i + dir_i, j + dir_j, score + 1
        best_routes.push(MazeState(straight_i, straight_j, direction, straight_score), from_state=best_state)

        # Turn left, without moving
        left_dir, left_score = (-dir_j, dir_i), score + 1000
        best_routes.push(MazeState(i, j, left_dir, left_score), from_state=best_state)

        # Turn right, without moving
        right_dir, right_score = (dir_j, -dir_i), score + 1000
        best_routes.push(MazeState(i, j, right_dir, right_score), from_state=best_state)


    # Using the graph, count the number of nodes reachable from the end cell
    # This is the number of nodes that are present in ALL best paths from start to end cell
    visited = set()
    to_visit = [best_end_state]
    while to_visit:
        i, j, direction, score, prev_states = to_visit.pop()
        visited.add((i, j))
        to_visit.extend(prev_state for prev_state in prev_states if prev_state is not None)
    return len(visited)


def main(filename: str = 'aoc_16.txt', expected: int = None):
    maze = read_input(filename)
    result = solve_maze(maze)    

    print(f'{filename=}')
    print(f'{result=}')
    print()

    assert expected is None or expected == result, \
            f'Expected {expected}, got {result}'


if __name__ == '__main__':
    main('aoc_16_example_0.txt', 45)
    main('aoc_16_example_1.txt', 64)
    main()
