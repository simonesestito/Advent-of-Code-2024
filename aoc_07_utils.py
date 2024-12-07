'''
Common utility functions for both parts of day 7
'''

from typing import TypeAlias, Generator, Callable, Iterable
from tqdm import tqdm


Equation: TypeAlias = tuple[int, list[int]]
Operator: TypeAlias = Callable[[int, int], int]


def read_input(filename: str = 'aoc_07.txt') -> Generator[Equation, None, None]:
    with open(filename) as f:
        for line in f:
            line = line.strip()

            result, operands = line.split(': ')
            operands = [ int(op) for op in operands.split() ]
            yield int(result), operands


def can_evaluate(
        result: int,
        operands: list[int],
        all_operators: list[Operator],
        partial_result: int = None
    ) -> bool:
    if partial_result is None:
        partial_result, operands = operands[0], operands[1:]

    # Try to evaluate with every symbol,
    # as long as the partial result is not above the final result
    if partial_result > result:
        return False

    # We have finished assigning operators
    if len(operands) == 0:
        return partial_result == result

    next_operand = operands[0]

    # Assign the next operators
    for op in all_operators:
        new_result = op(partial_result, next_operand)
        if can_evaluate(result, operands[1:], all_operators, new_result):
            return True

    return False  # It won't work with any next operators assignment


def sum_valid_results(inputs: Iterable[Equation], all_operators: list[Operator]) -> int:
    count = 0
    for result, operands in tqdm(inputs):
        if can_evaluate(result, operands, all_operators):
            count += result
    return count

