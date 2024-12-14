class Robot:
    def __init__(self, pos_x: int, pos_y: int, vel_x: int, vel_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = vel_x
        self.vel_y = vel_y

    def step(self, rows: int, cols: int, steps: int = 1):
        self.pos_x = (self.pos_x + self.vel_x * steps) % cols
        self.pos_y = (self.pos_y + self.vel_y * steps) % rows


def read_input(filename: str = 'aoc_13.txt') -> list[Robot]:
    robots: list[Robot] = []

    with open(filename) as f:
        for line in f:
            # p=0,4 v=3,-3
            line = line.strip()

            # p=0,4
            # v=3,-3
            pos_xy, vel_xy = line.split(' ')

            pos_x, pos_y = map(int, pos_xy[2:].split(','))
            vel_x, vel_y = map(int, vel_xy[2:].split(','))

            robots.append(Robot(pos_x, pos_y, vel_x, vel_y))

    return robots


def step_robots(robots: list[Robot], rows: int, cols: int, steps: int = 1):
    for robot in robots:
        robot.step(rows, cols, steps)

