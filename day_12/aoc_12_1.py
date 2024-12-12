from collections import defaultdict
from aoc_12_utils import read_input, find_regions, compute_area, Region


def compute_perimeter(region: Region) -> int:
    '''
    Compute the perimeter in an incremental way, cell by cell.
    Adapting to any shape of regions.
    '''
    perimeter = 0
    for i, j in region:
        # Add the border of this cell, individually
        perimeter += 4

        up_i, up_j = i - 1, j
        if (up_i, up_j) in region:
            # Remove the upper border of this cell
            # and the bottom border of the cell above
            perimeter -= 2

        left_i, left_j = i, j - 1
        if (left_i, left_j) in region:
            # Remove the left border of this cell
            # and the right border of the cell on the left
            perimeter -= 2

    return perimeter


def compute_price(region: Region) -> int:
    area = compute_area(region)
    perimeter = compute_perimeter(region)
    return area * perimeter


def main(filename: str = 'aoc_12.txt', expected: int = None):
    plot = read_input(filename)
    regions = find_regions(plot)
    
    result = sum(compute_price(region) for region in regions)

    if expected is None:
        print(result)
    elif expected != result:
        raise ValueError(f'{filename}: expected={expected}, result={result}')


if __name__ == '__main__':
    main('aoc_12_example_0.txt', 140)
    main('aoc_12_example_1.txt', 772)
    main('aoc_12_example_2.txt', 1930)
    main()
