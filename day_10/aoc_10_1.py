from aoc_10_utils import read_input, find_trailheads, Matrix, Point


def get_score_for_trail(matrix: Matrix, head: Point, visited: set[Point] = None) -> int:
    # Default argument assignment
    if visited is None:
        visited = { head }

    # Where do we have to go next?
    i, j = head
    next_value = matrix[i][j] + 1

    # Base case: we want next value = 10
    # This means that the caller of this cell, wanted a 9
    # and we are indeed a 9.
    # Also, since it called us, this means that we have
    # not been visited before, so no duplicates.
    if next_value == 10:
        return 1 if matrix[i][j] == 9 else 0

    score = 0

    # For every possible move...
    for diff_i, diff_j in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        next_i, next_j = i + diff_i, j + diff_j
        next_head = (next_i, next_j)
            
        # Skip invalid values, or already visited heads
        if next_i < 0 or next_j < 0 or next_i >= len(matrix) or next_j >= len(matrix[0]) or next_head in visited:
            continue

        next_head_value = matrix[next_i][next_j]

        # Visit only next value
        if next_value == next_head_value:
            # Mark as visited
            visited.add(next_head)
            score += get_score_for_trail(matrix, next_head, visited)
                
    return score


def main():
    matrix = read_input()
    trailheads = find_trailheads(matrix)
    scores_per_head = (get_score_for_trail(matrix, head) for head in trailheads)

    result = sum(scores_per_head)
    print(result)


if __name__ == '__main__':
    main()

