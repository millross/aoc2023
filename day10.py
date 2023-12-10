from common import aoc_23_common as aoc_23
from common.position import Position

class Grid:

    def __init__(self, filename):
        self._lines = aoc_23.load_file(filename)

    def find_first_instance_of(self, grid_value):
        for row, line in enumerate(self._lines):
            if (START_CHARACTER in line):
                return Position(line.find(START_CHARACTER), row)
        # Not found
        return None

    def has_pipe(self, position):
        return self._lines[position.y][position.x] in "-|FLJ7"
    
    def adjacent_pipes(self, position):
        above = Position(position.x, position.y - 1)
        below = Position(position.x, position.y + 1)
        left = Position(position.x - 1, position.y)
        right = Position(position.x + 1, position.y)

        potential_exits = filter(lambda pos: pos.x >= 0 and pos.y >= 0 and pos.x < len(self._lines[pos.y]) and pos.y < len(self._lines), [above, below, left, right])
        potential_exits_with_pipes = filter(lambda pos: self.has_pipe(pos), potential_exits)
        return potential_exits_with_pipes

START_CHARACTER = "S"

class LoopSeeker:
    def __init__(self, grid):
        self.grid = grid

    def find_start(self):
        return self.grid.find_first_instance_of(START_CHARACTER)

    def possible_start_exit_positions(self, start_pos):
        potential_exits_with_pipes = self.grid.adjacent_pipes(start_pos)
        # This includes pipes we cannot access e.g. horizontal pipe immediately below, so we need to filter further
        return potential_exits_with_pipes
    
    def valid_exit_for_relative_position(self, current_pos, pipe_pos):
        x_diff = pipe_pos.x - current_pos.x
        y_diff = pipe_pos.y - current_pos.y

        assert((abs(x_diff) == 1 and y_diff == 0) or (abs(y_diff) == 1 and x_diff == 0))

        
    

# Find the next position in the loop (use previous position to rule out one exit)
def find_next(current, seeker, route):
    # Are we the start, if so we have multiple new positions, we will just pick the first we find looking clockwise from top,
    # otherwise we can infer from existing character
    if len(route) == 0:
        return seeker.possible_start_exit_positions(current)
    return None



def find_loop(start):
    loop = [start]
    return loop



test_grid = Grid("day10_test_input_1")
test_seeker = LoopSeeker(test_grid)
test_start_position = test_seeker.find_start()
assert(test_start_position == Position(1, 1))
print(list(test_seeker.possible_start_exit_positions(test_start_position)))