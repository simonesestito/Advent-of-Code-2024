'''
Idea: walk in the matrix, saving the states of the walk = (i, j, step_i)
A loop is occuring for sure if we can find the same state again.

Try all possible additions of obstacles and see if we can find a loop.
'''

from aoc_06_utils import Matrix, read_input
from typing import TypeAlias, Generator
import multiprocessing  # I know, this solution is BAD
import sys

WalkState: TypeAlias = tuple[int, int, int]

steps = [ (-1, 0), (0, 1), (1, 0), (0, -1) ]


def is_matrix_looping(matrix: Matrix, i: int, j: int, step_i: int) -> bool:
    '''
    Walk in the matrix and see if we can find a loop
    '''
    past_states: set[WalkState] = set()

    max_i, max_j = len(matrix), len(matrix[0])

    # Make a step ahead
    diff_i, diff_j = steps[step_i]
    i, j = i + diff_i, j + diff_j

    # Loop and keep walking
    while -1 < i < max_i and -1 < j < max_j:
        curr_state: WalkState = (i, j, step_i)
        if curr_state in past_states:
            # We found a loop
            return True
        past_states.add(curr_state)

        cell = matrix[i][j]
        if cell == '#':
            # We found an obstacle
            # Go back
            i, j = i - diff_i, j - diff_j
            # Rotate the direction
            step_i = (step_i + 1) % 4

        # Make a step ahead
        diff_i, diff_j = steps[step_i]
        i, j = i + diff_i, j + diff_j


def count_obstacles_for_loop(matrix: Matrix, init_i: int, init_j: int, step_i: int, from_row: int = 0, to_row: int = None) -> Generator[int, None, None]:
    '''
    Count the number of obstacles that can be added to the matrix,
    in order to make the cursor stuck in a loop
    '''
    if to_row is None:
        to_row = len(matrix)
    to_row = min(to_row, len(matrix))  # Make sure we don't go out of bounds

    # Try all possible additions of obstacles
    #! This is BAD
    for i in range(from_row, to_row):
        row = matrix[i]
        for j, cell in enumerate(row):
            if cell == '.':
                # Try to add an obstacle and see if we can find a loop
                matrix[i][j] = '#'
                if is_matrix_looping(matrix, init_i, init_j, step_i):
                    yield 1
                matrix[i][j] = '.'


def _single_process_main(from_row: int, to_row: int):
    '''
    Run in parallel
    '''
    matrix, init_i, init_j, step_i = read_input()
    partial_result = sum(count_obstacles_for_loop(matrix, init_i, init_j, step_i, from_row, to_row))
    print(partial_result)


def main():
    # Run the BAD solution in parallel
    all_cpu_cores = max(1, multiprocessing.cpu_count() - 2)

    matrix, _, _, _ = read_input()
    rows_count = len(matrix)

    rows_per_process = int(rows_count / all_cpu_cores)
    print(f'Running on {all_cpu_cores} cores, {rows_per_process} rows per process', file=sys.stderr)

    processes = []
    for process_i in range(all_cpu_cores):
        from_row = process_i * rows_per_process
        to_row = from_row + rows_per_process if process_i < all_cpu_cores - 1 else rows_count
        print(f'Starting process {process_i} for rows {from_row} to {to_row}', file=sys.stderr)
        process = multiprocessing.Process(target=_single_process_main, args=(from_row, to_row))
        process.start()
        processes.append(process)
    
    print('\nFinal solution is the sum of all partial results printed out below\n', file=sys.stderr)
    # To directly have the final result in the console,
    # you can pipe this script with:
    # awk '{s+=$1} END {print s}'
    #
    # For example: python aoc_06_2.py | awk '{s+=$1} END {print s}'

    for process in processes:
        process.join()


if __name__ == '__main__':
    main()
