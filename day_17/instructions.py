from abc import ABC, abstractmethod

class Instruction(ABC):
    opcode: int
    literal: int

    def __init__(self, opcode: int, literal: int):
        self.opcode = opcode
        self.literal = literal

    @staticmethod
    def from_ops(opcode: int, literal: int) -> 'Instruction':
        all_instructions = [ ADV, BXL, BST, JNZ, BXC, OUT, BDV, CDV ]
        return all_instructions[opcode](literal)

    @abstractmethod
    def execute(self, state: 'StateMachine'):
        pass

    def _print_combo(self) -> str:
        match self.literal:
            case num if 0 <= num <= 3: return num
            case 4: return 'A'
            case 5: return 'B'
            case 6: return 'C'
            case _: raise ValueError(f'Invalid literal {self.literal}')

    def __iter__(self):
        yield self.opcode
        yield self.literal


class ADV(Instruction):
    def __init__(self, literal: int):
        super().__init__(0, literal)

    def execute(self, state: 'StateMachine'):
        combo = state.resolve_combo(self.literal)
        state.a = state.a >> combo

    def __str__(self):
        return f'A = A >> {self._print_combo()}'


class BXL(Instruction):
    def __init__(self, literal: int):
        super().__init__(1, literal)

    def execute(self, state: 'StateMachine'):
        state.b = state.b ^ self.literal

    def __str__(self):
        return f'B = B ^ {self._print_combo()}'


class BST(Instruction):
    def __init__(self, literal: int):
        super().__init__(2, literal)

    def execute(self, state: 'StateMachine'):
        combo = state.resolve_combo(self.literal)
        state.b = combo % 8

    def __str__(self):
        return f'B = {self._print_combo()} % 8'


class JNZ(Instruction):
    def __init__(self, literal: int):
        assert literal % 2 == 0, 'Jump literal must be even'
        super().__init__(3, literal // 2)

    def execute(self, state: 'StateMachine'):
        if state.a:
            state.move_instruction_pointer(self.literal)

    def __str__(self):
        return f'IF A: jump to {self.literal}'

class BXC(Instruction):
    def __init__(self, literal: int):
        super().__init__(4, literal)

    def execute(self, state: 'StateMachine'):
        state.b = state.b ^ state.c

    def __str__(self):
        return 'B = B ^ C'

class OUT(Instruction):
    def __init__(self, literal: int):
        super().__init__(5, literal)

    def execute(self, state: 'StateMachine'):
        combo = state.resolve_combo(self.literal)
        state.print_output(combo % 8)

    def __str__(self):
        return f'Output {self._print_combo()} % 8'

class BDV(Instruction):
    def __init__(self, literal: int):
        super().__init__(6, literal)

    def execute(self, state: 'StateMachine'):
        state.b = state.a >> state.resolve_combo(self.literal)

    def __str__(self):
        return f'B = A >> {self._print_combo()}'

class CDV(Instruction):
    def __init__(self, literal: int):
        super().__init__(7, literal)

    def execute(self, state: 'StateMachine'):
        state.c = state.a >> state.resolve_combo(self.literal)

    def __str__(self):
        return f'C = A >> {self._print_combo()}'