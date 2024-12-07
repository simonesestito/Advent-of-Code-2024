'''
Common utility functions for both parts of day 6
'''
from typing import TypeAlias

# Define types for brevity
Matrix: TypeAlias = list[list[str]]  # The cell is just a char -- use list instead of str to support item assignment


def read_input(filename: str = 'aoc_06.txt') -> tuple[Matrix, int, int, int]:
    '''
    Read the input matrix, but also find the initial position of the cursor and its direction
    '''
    with open(filename) as f:
        matrix = [line.strip() for line in f.readlines()]
    
    # Make it a list of lists, to support item assignment
    matrix = [list(line) for line in matrix]

    init_i, init_j, step_i = _find_initial_position(matrix)
    return matrix, init_i, init_j, step_i


def _find_initial_position(matrix: Matrix) -> tuple[int, int, int]:
    '''
    Find the initial position of the cursor and its direction
    '''
    max_i, max_j = len(matrix), len(matrix[0])

    for i, line in enumerate(matrix):
        for step_i, cursor in enumerate(['^', '>', '<', 'v']):
            j = next((cell_idx for cell_idx, cell in enumerate(line) if cell == cursor), -1)
            if j > -1:
                return i, j, step_i

