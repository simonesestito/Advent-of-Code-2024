from typing import NamedTuple
from instructions import Instruction

class StateMachine:
    # The 3 registers
    a: int
    b: int
    c: int

    instruction_pointer: int
    output: list[int]
    should_increase_instruction_pointer: bool


    def __init__(self, a: int, b: int, c: int):
        self.a = a
        self.b = b
        self.c = c
        self.instruction_pointer = 0
        self.output = []

    def execute_all(self, instructions: list[Instruction]) -> str:
        while self.instruction_pointer < len(instructions):
            # Detect when to increase the instruction pointer
            self.should_increase_instruction_pointer = True

            # Execute the instruction
            instruction = instructions[self.instruction_pointer]
            instruction.execute(state=self)

            if self.should_increase_instruction_pointer:
                # Go to the next instruction, unless it was a successful jump operation
                self.instruction_pointer += 1

        return self.read_output()

    
    def move_instruction_pointer(self, new_pointer: int):
        self.instruction_pointer = new_pointer
        self.should_increase_instruction_pointer = False

    def read_output(self) -> str:
        return ','.join(map(str, self.output))

    def resolve_combo(self, literal: int) -> int:
        match literal:
            case num if 0 <= num <= 3: return num
            case 4: return self.a
            case 5: return self.b
            case 6: return self.c
            case _: raise ValueError(f'Invalid literal {literal}')

    def print_output(self, output: int):
        self.output.append(output)
