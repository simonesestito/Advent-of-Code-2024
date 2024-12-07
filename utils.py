def safe_matrix_get(matrix, i: int, j: int, default = None):
    '''
    Safely get a value from a matrix, even if the indexes are out of bounds.
    In that case, return the default value.
    '''

    if i < 0 or i >= len(matrix):
        return default

    if j < 0 or j >= len(matrix[i]):
        return default

    return matrix[i][j]
