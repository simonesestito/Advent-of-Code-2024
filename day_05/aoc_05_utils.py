'''
Common utilities for both parts of day 5
'''
from typing import TypeAlias, Generator
from collections import defaultdict

# Define types for brevity
Rules: TypeAlias = dict[int, set[int]]
Update: TypeAlias = list[int]


def _read_input_sections(filename: str) -> Generator[Rules|Update, None, None]:
    # Collect rules in a dict { page_i -> list[pages_before_i] }
    rules: Rules = defaultdict(set)

    in_rules = True  # Separate rules from updates

    with open(filename) as f:
        for line in f:
            line = line.strip()

            if not line:
                # When there is a double newline, we are done with the rules
                in_rules = False
                yield rules  # The first yield section is the rules
            elif in_rules:
                # Parse the rules
                prev, succ = map(int, line.split('|'))
                rules[prev].add(succ)
            else:
                # Parse the single update
                yield [int(x) for x in line.split(',')]


def read_input(filename: str = 'aoc_05.txt') -> tuple[Rules, Generator[Update, None, None]]:
    rules_or_updates_generator = _read_input_sections(filename)
    rules = next(rules_or_updates_generator)
    updates = rules_or_updates_generator  # The rest of the generator is updates
    return rules, updates


def test_valid_update(rules: Rules, update: Update) -> bool:
    prevs = set()  # The pages that have been updated, iterating over the update

    for page in update:
        req = rules[page]
        if len(req.intersection(prevs)) > 0:
            return False
        prevs.add(page)
    return True
