from aoc_17_utils import parse_ops_line, read_input
from state_machine import StateMachine


def main(filename: str = 'aoc_17.txt', expected: str = None):
    state, instructions = read_input(filename)
    result = state.execute_all(instructions)

    print(f'{filename=}')
    print(f'{result=}')
    print()

    assert expected is None or result == expected, \
        f'Expected {expected}, got {result}'


def test_instruction(program: str, a: int = 0, b: int = 0, c: int = 0, expected: str = '', expected_a: int = None, expected_b: int = None, expected_c: int = None):
    '''
    A small function to run some sanity checks on the instruction execution
    '''
    state = StateMachine(a=a, b=b, c=c)
    instructions = parse_ops_line(program)
    result = state.execute_all(instructions)

    assert result == expected, f'Expected {expected}, got {result}'

    assert expected_a is None or state.a == expected_a, f'Expected {expected_a}, got {state.a}'
    assert expected_b is None or state.b == expected_b, f'Expected {expected_b}, got {state.b}'
    assert expected_c is None or state.c == expected_c, f'Expected {expected_c}, got {state.c}'


if __name__ == '__main__':
    test_instruction(c=9, program='2,6', expected_b=1, expected_c=9)
    test_instruction(a=10, program='5,0,5,1,5,4', expected='0,1,2')
    test_instruction(a=2024, program='0,1,5,4,3,0', expected='4,2,5,6,7,7,7,7,3,1,0', expected_a=0)
    test_instruction(b=29, program='1,7', expected_b=26)
    test_instruction(b=2024, c=43690, program='4,0', expected_b=44354)

    main('aoc_17_example_0.txt', '4,6,3,5,6,3,5,2,1,0')
    main()
