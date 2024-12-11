from typing import TypeAlias, Iterator, Generator
from math import ceil, log10


BlinksCache: TypeAlias = list[dict[int, int]]


def read_input(filename: str = 'aoc_11.txt') -> Iterator[int]:
    with open(filename) as f:
        return ( int(x) for x in f.read().split() )


def digits_of(n: int) -> int:
    return max(1, int(ceil(log10(n + 1e-4))))


def compute_stones(stone: int, blinks: int = 25, cache: BlinksCache = None) -> int:
    # Base case, we have to blink no more
    if blinks == 0:
        return 1

    # Default arguments assignment
    if cache is None:
        cache = [ dict() for _ in range(blinks) ]

    # Use the cache, if possible
    if stone in cache[blinks - 1]:
        return cache[blinks - 1][stone]

    # Apply the rules!
    total_stones = sum(compute_stones(new_stone, blinks - 1, cache) for new_stone in blink(stone))

    # Cache the result for future use
    cache[blinks - 1][stone] = total_stones
    return total_stones


def blink(stone: int) -> Generator[int, None, None]:
    digits = digits_of(stone)

    if stone == 0:
        # Rule 1: stone is zero
        yield 1
    elif digits % 2 == 0:
        # Rule 2: stone has an even number of digits
        # Split in two
        split_pow = 10 ** (digits / 2)
        yield stone // split_pow
        yield stone % split_pow
    else:
        # Rule 3: default
        # Multiply by 2024
        yield stone * 2024


def main(times: int):
    stones = read_input()

    # Expand every stone, recursively, individually
    result = sum(compute_stones(stone, times) for stone in stones)
    print(f'Result after {times} blinks: {result}')


if __name__ == '__main__':
    main(times=25)
    main(times=75)

