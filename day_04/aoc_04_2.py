from aoc_04_utils import safe_matrix_get, read_matrix


def test_xmas_from_position(matrix: list[str], i: int, j: int) -> bool:
    # Analyze possible Cross-MAS starting from this cell (the center of MAS).
    if safe_matrix_get(matrix, i, j) != 'A':
        # The center of MAS must be an A.
        return False

    # Get the 4 sorrounding diagonal cells
    upper_left, upper_right, lower_left, lower_right = \
        safe_matrix_get(matrix, i - 1, j - 1), \
        safe_matrix_get(matrix, i - 1, j + 1), \
        safe_matrix_get(matrix, i + 1, j - 1), \
        safe_matrix_get(matrix, i + 1, j + 1)

    # Ensure that diagonal cells are only M and S.
    # We want that in the diagonals, there is at least one M and one S, and no other letters.
    all_diagonals = {upper_left, upper_right, lower_left, lower_right}
    if all_diagonals != {'M', 'S'}:
        return False

    # They must be diagonally-opposite M and S.
    return upper_left != lower_right and upper_right != lower_left


def count_xmas(matrix: list[str]) -> int:
    count = 0
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if test_xmas_from_position(matrix, i, j):
                count += 1
    return count


def main():
    matrix = read_matrix()
    result = count_xmas(matrix)
    print(result)


if __name__ == '__main__':
    main()

