from state_machine import StateMachine
from instructions import Instruction


def read_input(filename: str) -> tuple[StateMachine, list[Instruction]]:
    '''
    From the input file, read:
    - state registers
    - instructions (operations) with literals (operands)
    '''
    with open(filename) as f:
        # Read 3 lines corresponding to the 3 registers
        def _read_register():
            line = f.readline().strip()
            return int(line.split(': ')[1])

        state = StateMachine(
            a=_read_register(),
            b=_read_register(),
            c=_read_register(),
        )

        # Skip an empty line
        f.readline()

        # Read the program instructions
        ops = parse_ops_line(f.readline().strip())

        return state, ops

def parse_ops_line(line: str) -> list[Instruction]:
    if ': ' in line:
        line = line.split(': ')[1]

    ops_line = [
        int(op)  # Operator or operand
        for op in line.split(',')
    ]

    # Split between operations and literal values
    instructions = ops_line[::2]
    literals = ops_line[1::2]

    return [
        Instruction.from_ops(op, literal)
        for op, literal in zip(instructions, literals)
    ]
