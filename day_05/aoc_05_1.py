from collections import defaultdict
from typing import TypeAlias, Generator
from aoc_05_utils import Rules, Update, read_input, test_valid_update

# Define types for brevity
Rules: TypeAlias = dict[int, set[int]]
Update: TypeAlias = list[int]


def take_middle_of_valid_updates(rules: Rules, updates: Generator[Update, None, None]) -> Generator[int, None, None]:
    for update in updates:
        if test_valid_update(rules, update):
            middle_page = update[len(update) // 2]
            yield middle_page


def main():
    rules, updates = read_input()
    valid_middle_pages = take_middle_of_valid_updates(rules, updates)
    result = sum(valid_middle_pages)
    print(result)


if __name__ == '__main__':
    main()
