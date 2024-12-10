from aoc_10_utils import read_input, find_trailheads, Matrix, Point


def get_rating_for_trail(matrix: Matrix, head: Point, ratings_cache: dict[Point, int] = None) -> int:
    '''
    Recursive function to calculate the rating of a trail.

    Args:
        matrix (Matrix): The matrix of the trail.
        head (Point): The current head of the trail.
        ratings_cache (dict[Point, int]): A dictionary to cache the ratings of the already ratings_cache trails.
    '''
    # Default argument assignment
    if ratings_cache is None:
        ratings_cache = dict()

    if head in ratings_cache:
        return ratings_cache[head]  # Return cached rating

    # Where do we want to go?
    i, j = head
    next_value = matrix[i][j] + 1

    # Base case: we want next value = 10
    # This means that the caller of this cell, wanted a 9
    # and we are indeed a 9.
    # This is the end of the graph walk
    if next_value == 10:
        return 0

    # Idea: rating = number of split at a certain point
    # in the graph walk, but -1 because we'll always go for sure
    # in at least 1 next cell.
    # So, the number of splits is the number of times we call this function recursively
    # in this step, -1 which is the default walk (no split).
    rating = -1

    # For every possible move...
    for diff_i, diff_j in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        next_i, next_j = i + diff_i, j + diff_j
        next_head = (next_i, next_j)
            
        # Skip invalid values
        if next_i < 0 or next_j < 0 or next_i >= len(matrix) or next_j >= len(matrix[0]):
            continue

        next_head_value = matrix[next_i][next_j]

        # Visit only next value
        if next_value == next_head_value:
            rating += get_rating_for_trail(matrix, next_head, ratings_cache) + 1
                
    ratings_cache[head] = rating  # Cache rating for next time
    return rating


def main():
    matrix = read_input()
    trailheads = find_trailheads(matrix)

    # Do +1 to the rating of each trailhead,
    # because we are counting the number of splits.
    # But every path always has 1 default walk, without ever splitting.
    ratings_per_head = (get_rating_for_trail(matrix, head) + 1 for head in trailheads)

    result = sum(ratings_per_head)
    print(result)


if __name__ == '__main__':
    main()

