from aoc_08_utils import FrequenciesTable, Coordinate, MapSize, iter_pairs, read_input, within_matrix_area
from typing import Generator


def identify_all_antinodes(freqs: FrequenciesTable) -> Generator[Coordinate, None, None]:
    for antennas in freqs.values():
        for (i0, j0), (i1, j1) in iter_pairs(antennas):
            diff_i, diff_j = i0 - i1, j0 - j1

            # Add an antinode at same distance from antenna 1
            yield i1 - diff_i, j1 - diff_j

            # Add an antinode at opposite distance from antenna 0
            yield i0 + diff_i, j0 + diff_j


def count_unique_antinodes(freqs: FrequenciesTable, size: MapSize) -> int:
    all_antinodes = identify_all_antinodes(freqs)
    return len({
        antinode
        for antinode in all_antinodes
        if within_matrix_area(size, antinode)
    })


def main():
    freqs, size = read_input()
    result = count_unique_antinodes(freqs, size)
    print(result)


if __name__ == '__main__':
    main()

