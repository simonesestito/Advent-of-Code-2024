from aoc_06_utils import Matrix, read_input

def walk_in_matrix(matrix: Matrix, i: int, j: int, step_i: int):
    '''
    Walk in the matrix, marking the visited cells with 'X'
    '''
    steps = [ (-1, 0), (0, 1), (1, 0), (0, -1) ]
    max_i, max_j = len(matrix), len(matrix[0])

    # Mark where we are at the beginning of the walk
    matrix[i][j] = 'X'

    # Make a step ahead
    diff_i, diff_j = steps[step_i]
    i, j = i + diff_i, j + diff_j

    # Loop and keep walking
    while -1 < i < max_i and -1 < j < max_j:
        cell = matrix[i][j]
        if cell == '#':
            # We found an obstacle
            # Go back
            i, j = i - diff_i, j - diff_j
            # Rotate the direction
            step_i = (step_i + 1) % 4
        else:
            # Mark the cell as visited
            matrix[i][j] = 'X'
        
        # Make a step ahead
        diff_i, diff_j = steps[step_i]
        i, j = i + diff_i, j + diff_j


def main():
    matrix, init_i, init_j, step_i = read_input()
    walk_in_matrix(matrix, init_i, init_j, step_i)
    result = sum(line.count('X') for line in matrix)
    print(result)


if __name__ == '__main__':
    main()
