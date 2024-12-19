from typing import Iterable
from collections import defaultdict


def read_input(filename: str) -> tuple[list[str], Iterable[str]]:
    f = open(filename)
    stripes = f.readline().strip().split(', ')

    def _read_designs() -> Iterable[str]:
        while line := f.readline():
            line = line.strip()
            if line:
                yield line
        f.close()

    designs = _read_designs()

    return stripes, designs


def optimize_stripes(stripes: list[str]) -> dict[str, list[str]]:
    stripes_dict = defaultdict(list)

    # Index by the first letter
    for stripe in stripes:
        stripes_dict[stripe[0]].append(stripe)

    # Sort by descending length
    for substripes in stripes_dict.values():
        substripes.sort(key=len, reverse=True)

    return stripes_dict


def solve_designs(stripes: list[str], designs: Iterable[str]) -> int:
    stripes_dict = optimize_stripes(stripes)
    cache = dict()
    return sum(1 for design in designs if solve_design(stripes_dict, design, cache))


def solve_design(stripes: dict[str, list[str]], design: str, cache: dict[str, bool]) -> bool:
    if not design:
        return True

    if design in cache:
        return cache[design]

    c = design[0]
    for stripe in stripes[c]:
        # Try with this stripe
        if design.startswith(stripe):
            # Found, keep going
            subdesign = design[len(stripe):]

            if solve_design(stripes, subdesign, cache):
                # Success, all design solved
                cache[design] = True
                return True

    cache[design] = False
    return False


def main(filename: str = 'aoc_19.txt', expected: int = None):
    stripes, designs = read_input(filename)
    result = solve_designs(stripes, designs)

    print(f'{filename=}')
    print(f'{result=}')
    print()

    assert expected is None or result == expected, \
        f'Expected {expected}, got {result}'


if __name__ == '__main__':
    main('aoc_19_example_0.txt', 6)
    main()

