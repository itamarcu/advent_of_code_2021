with open('day25.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

HEIGHT = len(lines)
WIDTH = len(lines[0])


def empty_grid():
    return [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]


grid = empty_grid()
next_grid = empty_grid()


def grid_at(x: int, y: int) -> str:
    return grid[y % HEIGHT][x % WIDTH]


def set_next_grid(x: int, y: int, value: str):
    next_grid[y % HEIGHT][x % WIDTH] = value


def print_grid():
    for y in range(HEIGHT):
        print(''.join(grid[y]))


for y in range(HEIGHT):
    line = lines[y]
    grid[y] = list(line)

step_i = 0
while True:
    step_i += 1
    something_moved = False
    # first move everything east
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid_at(x, y) == '>' and grid_at(x + 1, y) == '.':
                set_next_grid(x + 1, y, '>')
                something_moved = True
            elif grid_at(x, y) != '.':
                set_next_grid(x, y, grid_at(x, y))
    grid = next_grid.copy()
    next_grid = empty_grid()
    # then move everything south
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid_at(x, y) == 'v' and grid_at(x, y + 1) == '.':
                set_next_grid(x, y + 1, 'v')
                something_moved = True
            elif grid_at(x, y) != '.':
                set_next_grid(x, y, grid_at(x, y))
    grid = next_grid.copy()
    next_grid = empty_grid()
    if not something_moved:
        break

print(step_i)  # 453



