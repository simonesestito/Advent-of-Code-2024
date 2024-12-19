from state_machine import StateMachine, Instruction
from instructions import JNZ, OUT, ADV
from aoc_17_utils import read_input
from tqdm import tqdm
from typing import Generator


class StateMachineV2(StateMachine):
    '''
    An evoluted state machine, able to reset and assert a special output.
    '''
    def __init__(self):
        super().__init__(a=0, b=0, c=0)
        self.expected_output = []

    def reset(self, a: int, expected_output: list[int]):
        self.a, self.b, self.c = a, 0, 0
        self.instruction_pointer = 0
        self.output = []
        self.expected_output = expected_output

    def execute_all_and_verify_output(self, instructions: list[Instruction]) -> bool:
        '''
        Execute all instructions and verify the output.
        '''
        try:
            self.execute_all(instructions)
            return not self.expected_output
        except AssertionError:
            return False


    def print_output(self, output: int):
        if not self.expected_output:
            return
        assert self.expected_output, 'No more expected output'

        expected = self.expected_output[0]
        assert output == expected, f'Expected {expected}, got {output}'

        self.expected_output = self.expected_output[1:]
        self.output.append(output)


def find_last_bits_for_a(instructions: list[Instruction], steps: int, suffix: int) -> int:
    '''
    Find the last bits for register "A" that produces the program itself as output.
    '''
    # The output we are looking for
    expected_output = [ opcode_or_literal for instruction in instructions for opcode_or_literal in instruction ][:steps]

    # Create the state machine
    state = StateMachineV2()

    # Try all values for a, showing progress bar only in the first process
    a_prefix = 0
    for a_prefix in range(0b11111):
        suffix_len = 3 * steps
        a = a_prefix * 2 ** suffix_len + suffix
        state.reset(a=a, expected_output=expected_output)
        if state.execute_all_and_verify_output(instructions):
            return a
        a_prefix += 1
        print(f'{a=}', end='\r')
    return suffix


def find_initialization_for_a(instructions: list[Instruction]) -> int:
    '''
    Find the initial value for register "A" that produces the program itself as output.
    '''
    # The output we are looking for
    expected_output = [ opcode_or_literal for instruction in instructions for opcode_or_literal in instruction ]

    # Perform some optimizations
    a_range = assert_can_optimize(instructions, expected_output)

    suffix = 0
    for i in range(1, 5 * len(expected_output)):
        suffix = find_last_bits_for_a(instructions, steps=i, suffix=suffix)
        print(f'{suffix=:<16d} {bin(suffix)[2:]:>64s}')

    return suffix


def assert_can_optimize(instructions: list[Instruction], expected_output: list[int]):
    # There may be an optimization
    # If the program is a loop
    assert isinstance(instructions[-1], JNZ), 'The last instruction must be a JNZ'
    assert instructions[-1].literal == 0, 'The last instruction must jump to the beginning'

    # and register A is assigned only once
    a_assignments = [instruction for instruction in instructions if str(instruction).startswith('A = ')]
    assert len(a_assignments) == 1, 'Register A must be assigned only once'

    # and there is only one output per loop iteration
    output_instructions = [instruction for instruction in instructions if isinstance(instruction, OUT)]
    assert len(output_instructions) == 1, 'There must be only one output per loop iteration'
    
    # then, we can define some limits for a
    
    # We have to loop a few known times = len(instructions) * 2, because
    # each iteration outputs a value (remember that an instruction is an operation and a literal)
    loop_times = len(expected_output)

    # Now, we have to analyze the assignments to register A
    a_assignment = a_assignments[0]
    assert isinstance(a_assignment, ADV), 'The assignment must be an ADV'

    # a_shifted_by = a_assignment.literal

    # # We know that A must be sufficiently large to be shifted this number of times
    # # without resulting in zero (otherwise the program would end and not loop)
    # min_a = 2 ** (a_shifted_by * (loop_times - 1))
    # max_a = 2 ** (a_shifted_by * 7)  # FIXME: use the actual number of loop iterations
    # return range(int(min_a), int(max_a))


def main(filename: str = 'aoc_17.txt', expected: str = None):
    _, instructions = read_input(filename)
    for i, instruction in enumerate(instructions):
        print(f'[{i}]', instruction)
    print()

    result = find_initialization_for_a(instructions)

    print(f'{filename=}')
    print(f'{result=}')
    print()

    for i, instruction in enumerate(instructions):
        print(f'[{i}]', instruction)
    print()

    assert expected is None or result == expected, \
        f'Expected {expected}, got {result}'


if __name__ == '__main__':
    main('aoc_17_example_1.txt', 117440)
    # FIXME main()
