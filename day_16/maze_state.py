from aoc_16_utils import Direction

MazeStateKey = tuple[int, int, Direction]  # i, j, direction

class MazeState:
    i: int
    j: int
    direction: Direction
    score: int

    # For part 2: keep track of previous states to reach this one
    prev_states: list['MazeState']

    def __init__(self, i: int, j: int, direction: Direction, score: int):
        self.i = i
        self.j = j
        self.direction = direction
        self.score = score
        self.prev_states = []

    def __lt__(self, other: 'MazeState') -> bool:
        return self.score < other.score

    def as_key(self) -> MazeStateKey:
        return self.i, self.j, self.direction

    def __iter__(self):
        return iter((self.i, self.j, self.direction, self.score, self.prev_states))

    def __eq__(self, other: 'MazeState') -> bool:
        if not isinstance(other, MazeState):
            return False
        return self.i == other.i and self.j == other.j and self.direction == other.direction
