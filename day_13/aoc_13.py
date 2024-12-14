from typing import NamedTuple, Generator

A_COST = 3

B_COST = 1


class Game(NamedTuple):
    '''
    Structure to save data about a game.
    '''
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    win_x: int
    win_y: int


def read_input(filename: str = 'aoc_13.txt', win_offset: int = 0) -> Generator[Game, None, None]:
    with open(filename) as f:
        while True:
            # There are 3 lines with all data about a game
            line_a = f.readline().strip()
            line_b = f.readline().strip()
            line_win = f.readline().strip()

            if not line_a:
                break

            # Also, after looking at the input,
            # we can see that the numbers are always positive
            # this may simplify our solution
            yield Game(
                a_x=int(line_a.split(',')[0][11:]),
                a_y=int(line_a.split(',')[1][2:]),
                b_x=int(line_b.split(',')[0][11:]),
                b_y=int(line_b.split(',')[1][2:]),
                win_x=int(line_win.split(',')[0][9:]) + win_offset,
                win_y=int(line_win.split(',')[1][3:]) + win_offset,
            )

            # Skip one empty line in the input file
            f.readline()


def find_meetpoint(game: Game):
    '''
    We can interpret this problem as a System of Linear Equations.

    - n_a (or n_b) is the number of times we have to press button A (or B)
    - a_x is the increment that pressing button A will give to X, and so on
    - win_x (and win_y) is our goal point in the space.

    The system of linear equation that we have is:
    {  n_a * a_x + n_b * b_x = win_x
       n_a * a_y + n_b * b_y = win_y
    Our unknown variables are n_a and n_b (2 variables).
    We can solve it since we have 2 distinct equations.

    A simple solution is available when interpreting this system in matrix formulation,
    which is what follows.

    I decided not to use Numpy 
    '''

    a_x, a_y, b_x, b_y, win_x, win_y = game

    det_A = a_x * b_y - a_y * b_x
    
    # Check if the determinant is zero (no unique solution)
    assert det_A != 0
    
    # Calculate the inverse of matrix A manually
    inv_A = [
        [b_y / det_A, -b_x / det_A],
        [-a_y / det_A, a_x / det_A]
    ]
    
    # Solve for n_a and n_b using the formula X = A^-1 * B
    n_a = inv_A[0][0] * win_x + inv_A[0][1] * win_y
    n_b = inv_A[1][0] * win_x + inv_A[1][1] * win_y
   
    # We said that the unknown variables must be integers,
    # so try with the nearest integer
    # 
    # Due to floating point approximation, n_a may be 0.9999 or 1.0001, which are both 1
    n_a, n_b = round(n_a), round(n_b)

    reconstruct_x = n_a*a_x+n_b*b_x
    reconstruct_y = n_a*a_y+n_b*b_y

    if reconstruct_x != win_x or reconstruct_y != win_y:
        return None
   
    # We got the solution to the system! Compute the cost
    min_cost = n_a * A_COST + n_b * B_COST
    return min_cost


def main(filename: str = 'aoc_13.txt', win_offset: int = 0, expected: int = None):
    games = read_input(filename, win_offset)

    all_costs = (find_meetpoint(game) for game in games)
    result = sum(cost or 0 for cost in all_costs)

    print(f'{filename=}')
    print(f'{win_offset=}')
    print(f'{result=}')
    print()
    
    if expected is not None and result != expected:
        raise ValueError(f'Error processing {filename}: {result=}, {expected=}')


if __name__ == '__main__':
    main('aoc_13_example.txt', expected=480)
    main(expected=40069)
    main(win_offset=10000000000000)

