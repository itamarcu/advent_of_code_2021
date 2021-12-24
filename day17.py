
# trying to manually calculate without code
from re import fullmatch

with open('day17.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]
# target area: x=117..164, y=-140..-89
min_x, max_x, min_y, max_y = [int(x) for x in fullmatch(r'target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)', lines[0]).groups()]

possible_x_speeds = []
for xs in range(1, max_x+1):  # max_x is technically highest, but obviously not best answer
    # try increasing xs one by one until we probably don't have a good solution (for maximum height)
    x_coords_we_will_stop_at = [0]
    for x in range(xs, 0, -1):
        x_coords_we_will_stop_at.append(x_coords_we_will_stop_at[-1] + x)
    if any(min_x <= x <= max_x for x in x_coords_we_will_stop_at):
        possible_x_speeds.append(xs)


possible_y_speeds = []
for ys in range(min_y, 999):  # kinda guessing at reasonable bounds here
    # try increasing ys one by one until we definitely shoot past target
    y_coords_we_will_stop_at = [0]
    y = 0
    y_velocity = ys
    while y >= min_y:
        y += y_velocity
        y_velocity -= 1
        if min_y <= y <= max_y:
            possible_y_speeds.append(ys)
            break

total_answers = 0
best_result = (-999, -999, -999)  # best xs, best ys, best height
for xs in possible_x_speeds:
    for ys in possible_y_speeds:
        xv, yv = xs, ys
        x, y = 0, 0
        highest_y = 0
        while True:
            x, y = x + xv, y + yv
            xv -= 1 if xv > 0 else -1 if xv < 0 else 0
            yv -= 1
            highest_y = max(highest_y, y)
            if min_x <= x <= max_x and min_y <= y <= max_y:
                # possible answer, check if better than best so far
                if best_result[2] < highest_y:
                    best_result = xs, ys, highest_y
                total_answers += 1
                break
            if x > max_x or y < min_y:
                # overshot
                break

print(best_result)
print(total_answers)  # not 360