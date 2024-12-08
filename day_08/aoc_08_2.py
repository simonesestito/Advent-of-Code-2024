from aoc_08_utils import FrequenciesTable, Coordinate, MapSize, iter_pairs, read_input, within_matrix_area
from typing import Generator
import sys


def identify_all_antinodes(freqs: FrequenciesTable, size: MapSize) -> Generator[Coordinate, None, None]:
    for antennas in freqs.values():
        for (i0, j0), (i1, j1) in iter_pairs(antennas):
            # There are also antinodes on every antenna
            yield i0, j0
            yield i1, j1

            # Compute the interval of the antinodes
            # = distance between this pair of antennas
            diff_i, diff_j = i0 - i1, j0 - j1

            # Make one step ahead in that interval
            i0, j0, i1, j1 = \
                    i0 + diff_i, \
                    j0 + diff_j, \
                    i1 - diff_i, \
                    j1 - diff_j

            # Repeat for antenna 0 until out of map
            while within_matrix_area(size, (i0, j0)):
                yield i0, j0
                i0 += diff_i
                j0 += diff_j

            # Repeat for antenna 1 until out of map
            while within_matrix_area(size, (i1, j1)):
                yield i1, j1
                i1 -= diff_i
                j1 -= diff_j


def count_unique_antinodes(freqs: FrequenciesTable, size: MapSize) -> int:
    all_antinodes = identify_all_antinodes(freqs, size)
    return len({
        antinode
        for antinode in all_antinodes
    })


def visualize_resulting_antinodes(test_filename: str = 'aoc_08_example.txt'):
    freqs, size = read_input(test_filename)

    matrix = [
        [ '.' for _ in range(size[1]) ]
        for _ in range(size[0])
    ]

    for freq, antennas in freqs.items():
        for i, j in antennas:
            matrix[i][j] = freq

    for i, j in identify_all_antinodes(freqs, size):
        if within_matrix_area(size, (i, j)):
            matrix[i][j] = '#'

    for row in matrix:
        print(''.join(row), file=sys.stderr)

    test_result = count_unique_antinodes(freqs, size)
    print('\nResult for test input:', test_result, end='\n\n', file=sys.stderr, flush=True)


def main():
    visualize_resulting_antinodes()

    freqs, size = read_input()
    result = count_unique_antinodes(freqs, size)
    print(result)


if __name__ == '__main__':
    main()

