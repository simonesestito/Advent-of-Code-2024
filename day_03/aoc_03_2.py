import re
from typing import Generator


def read_input(filename: str = 'aoc_03.txt') -> str:
    with open(filename, 'r') as file:
        return file.read()


def find_actual_operations(input_str: str) -> Generator[str, None, None]:
    cursor = 0  # Where we are in the string, after the last elaboration
                # We do not split and merge parts of the string, to keep the solution more optimized

    while cursor < len(input_str):
        dont_i = input_str.find("don't()", cursor)
        if dont_i == -1:
            break

        yield input_str[cursor:dont_i]
        
        do_i = input_str.find('do()', dont_i)
        if do_i == -1:
            # No more do()s, so we don't have to do anything else
            cursor = len(input_str)
            break

        # Add the length of do() itself to the cursor
        cursor = do_i + 4

    # Elaborate the last part of the string
    if cursor < len(input_str):
        yield input_str[cursor:]


def find_mul(input_str: str) -> Generator[int, None, None]:
    for match in re.findall(r'mul\(\d{1,3},\d{1,3}\)', input_str):
        # Extract the two numbers from the match
        a, b = map(int, match[4:-1].split(','))
        yield a * b


def main():
    input_str = read_input()
    actual_operations = find_actual_operations(input_str)

    # Use a standard for to make it more readable
    result = 0
    for inner_operations in actual_operations:
        inner_result = sum(find_mul(inner_operations))
        result += inner_result
        
    print(result)


if __name__ == '__main__':
    main()