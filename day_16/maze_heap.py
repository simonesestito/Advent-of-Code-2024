import heapq
from aoc_16_utils import Maze
from maze_state import MazeState


class MazeHeap:
    def __init__(self, maze: Maze):
        self.maze = maze
        self._heap: list[MazeState] = []
        self._in_heap: dict[MazeStateKey, MazeState] = dict()  # key -> state with the min score known so far


    def push(self, state: MazeState, from_state: MazeState | None = None):
        ## from_state is used only in part 2

        # Ignore invalid cells (walls)
        if self.maze[state.i][state.j] == '#':
            return

        state.prev_states.append(from_state)

        # Do not process the same cell twice, if the score is higher or equal to what we already have seen before
        key = state.as_key()
        if key in self._in_heap:
            # Handle duplicates
            if state.score > self._in_heap[key].score:
                # Skip this state: the score is higher to what we already have seen before
                return
            if state.score == self._in_heap[key].score:
                # Skip this state: the score is equal to what we already have seen before
                # Still, keep track of this other path (Part 2 only!)
                self._in_heap[key].prev_states.append(from_state)
                return
            
            # Update the score of the state in the heap: this insertion is better!
            # -> remove the old state from the heap
            old_state = next(s for s in self._heap if s.as_key() == key)
            self._heap.remove(old_state)
            heapq.heapify(self._heap)

        # Also, do not go in the opposite direction as the one we came from
        # If there is a visit in the same cell, but in the opposite direction, we can skip it
        opposite_direction = (-state.direction[0], -state.direction[1])
        opposite_key = state.i, state.j, opposite_direction
        if opposite_key in self._in_heap and state.score > self._in_heap[opposite_key].score:
            return False

        # Finally, add the state to the heap
        self._in_heap[key] = state
        heapq.heappush(self._heap, state)
        return True

    def pop(self) -> MazeState:
        return heapq.heappop(self._heap)

    def __len__(self) -> int:
        return len(self._heap)

    def empty(self) -> bool:
        return len(self) == 0

    def __bool__(self) -> bool:
        return not self.empty()
