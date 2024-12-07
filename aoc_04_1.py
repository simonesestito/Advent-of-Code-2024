from utils import safe_matrix_get


def read_matrix(filename: str = 'aoc_04.txt') -> list[str]:
    with open(filename, 'r') as file:
        return [l.strip() for l in file.readlines()]


def count_xmas(matrix: list[str]) -> int:
    count = 0
    # Use a standard nested for-loop instead of a list comprehension
    # to make the code much more readable.
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            # Count the number of XMAS starting from this cell.
            count += count_xmas_from_position(matrix, i, j)
    return count


def count_xmas_from_position(matrix: list[str], i: int, j: int) -> int:
    # Analyze possible XMAS starting from this cell.

    all_directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),  # Skip (0, 0) because it means no movement.
        (1, -1), (1, 0), (1, 1),
    ]

    # For any possible direction, we still have to start with an X (= the first letter of XMAS).
    if safe_matrix_get(matrix, i, j) != 'X':
        return 0

    count = 0
    for step_i, step_j in all_directions:
        if search_xmas_in_position_with_direction(matrix, i, j, step_i, step_j):
            # We found the word XMAS in this direction, starting from this cell.
            count += 1
    return count


def search_xmas_in_position_with_direction(matrix: list[str], i: int, j: int, step_i: int, step_j: int) -> bool:
    for char in 'MAS':  # We already know the first letter is X.
        # Keep moving in the same direction, indicated by step_i and step_j.
        i += step_i
        j += step_j

        # Check if the current cell contains the expected letter.
        if safe_matrix_get(matrix, i, j) != char:
            return False

    return True


def main():
    matrix = read_matrix()
    result = count_xmas(matrix)
    print(result)


if __name__ == '__main__':
    main()

