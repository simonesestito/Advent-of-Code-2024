from aoc_12_utils import read_input, find_regions, compute_area, Region, Coordinate
import sys


def compute_sides(region: Region, visited: set[Coordinate] = None, i: int = None, j: int = None, verbose: bool = False) -> int:
    def _print(text: str):
        if verbose:
            print(text, file=sys.stderr, flush=True)

    # Default arguments assignment
    if visited is None:
        visited = set()
        i, j = min(region)

    # Avoid double counting and errors
    if (i, j) in visited or (i, j) not in region:
        return 0
    visited.add((i, j))  # Mark as visited

    # List all possible sides, in general
    vertical_sides = { (0, 1), (0, -1) }
    horizontal_sides = { (1, 0), (-1, 0) }
    all_sides = vertical_sides.union(horizontal_sides)

    # Count all the sides that I have (my borders)
    my_sides = set()
    for side in all_sides:
        diff_i, diff_j = side
        next_i, next_j = i + diff_i, j + diff_j

        if (next_i, next_j) not in region:
            # No block of the same region in this direction.
            # This implies that I have this side as a border of the region!
            my_sides.add(side)

    # Delete vertical and horizontal sides that I don't have
    vertical_sides = vertical_sides.intersection(my_sides)
    horizontal_sides = horizontal_sides.intersection(my_sides)

    sides_count = 0  # Count of the UNIQUE sides that I have as region borders

    # For all the sides that I have as region borders,
    # I can count a specific side only if allowed by neighbours
    #
    # It is allowed by my neighbours if they don't have the same side
    #
    # More specifically:
    # - count vertical sides if I don't have an upper neighbour that has it (only the upper neighbour in the line can have it)
    # - count horizontal sides if I don't have a left neighbour that has it (only the leftmost neighbour in the line can have it)
    for vertical_side in vertical_sides:
        diff_i, diff_j = vertical_side

        # I can allow a vertical side only if I don't have
        # an upper neighbour that has it
        upper_i, upper_j = i - 1, j
        if (upper_i, upper_j) not in region:
            # This must be a side because I don't have an upper neighbour
            sides_count += 1
            _print(f'({i}, {j}) has vertical side {vertical_side}')
        else:
            # Check if my upper neighbour has that vertical side that I want
            upper_side_i, upper_side_j = upper_i + diff_i, upper_j + diff_j
            # Tricky part: if I have the upper neighbour,
            #              I can count this side as mine, if I am the uppermost neighbour in the line,
            #              because the upper neighbour can't have it.
            #              This means that if I check this vertical_side (that I want for myself) on the upper neighbour,
            #              if that side is in the region, implies that my upper neighbour doesn't have it,
            #              so I am the uppermost neighbour, and I am the one that can count this unique side.
            #
            # Example: check for left side (0, -1) on the upper neighbour.
            #          If it is in the region, it means that the upper neighbour has a cell in the region on its left,
            #          so it can't have the left side as a region border, so I am the one that can count it.
            if (upper_side_i, upper_side_j) in region:
                sides_count += 1
                _print(f'({i}, {j}) has vertical side {vertical_side}')


    # Do the same, in a similar way, for horizontal sides
    for horizontal_side in horizontal_sides:
        diff_i, diff_j = horizontal_side

        # I can allow a horizontal side only if I don't have
        # a left neighbour that has it
        left_i, left_j = i, j - 1
        if (left_i, left_j) not in region:
            sides_count += 1
            _print(f'({i}, {j}) has horizontal side {horizontal_side}')
        else:
            # Check if my left neighbour has that horizontal side that I want
            # Tricky part follows the same logic as for vertical sides, in a specular way
            left_side_i, left_side_j = left_i + diff_i, left_j + diff_j
            if (left_side_i, left_side_j) in region:
                sides_count += 1
                _print(f'({i}, {j}) has horizontal side {horizontal_side}')

    _print(f'Sides of ({i}, {j}): {sides_count=}')

    # Now, go to my neighbours and repeat, adding their UNIQUE sides to my count
    for diff_i, diff_j in all_sides:
        next_i, next_j = i + diff_i, j + diff_j
        sides_count += compute_sides(region, visited, next_i, next_j, verbose)

    return sides_count


def compute_price(region: Region) -> int:
    area = compute_area(region)
    sides = compute_sides(region)
    return area * sides


def main(filename: str = 'aoc_12.txt', expected: int = None):
    plot = read_input(filename)
    regions = find_regions(plot)
    
    result = sum(compute_price(region) for region in regions)

    if expected is None:
        print(result)
    elif expected != result:
        raise ValueError(f'{filename}: expected={expected}, result={result}')


if __name__ == '__main__':
    main('aoc_12_example_0.txt', 80)
    main('aoc_12_example_1.txt', 436)
    main('aoc_12_example_2.txt', 1206)
    main('aoc_12_example_3.txt', 236)
    main('aoc_12_example_4.txt', 368)
    main()
