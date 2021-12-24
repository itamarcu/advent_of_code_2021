
with open('day9.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

height_map = []
for line in lines:
    height_map.append([int(c) for c in line])

HEIGHT = len(height_map)
WIDTH = len(height_map[0])
NEIGHBOR_DIFFS = [(-1, 0), (0, -1), (+1, 0), (0, +1)]
MAX_HEIGHT = 9

total_risk_level_sum = 0
low_points = []
for y in range(HEIGHT):
    for x in range(WIDTH):
        spot_h = height_map[y][x]
        is_low_point = True
        for y_diff, x_diff in NEIGHBOR_DIFFS:
            y2 = y + y_diff
            x2 = x + x_diff
            if x2 >= 0 and y2 >= 0 and x2 < WIDTH and y2 < HEIGHT and height_map[y2][x2] <= spot_h:
                is_low_point = False
                break  # optimization!
        if is_low_point:
            risk_level = spot_h + 1
            total_risk_level_sum += risk_level
            low_points.append((y, x))

print(total_risk_level_sum)  # 478

######## part 2

basin_sizes = []
for low_point in low_points:
    frontier = [low_point]
    visited = {low_point}
    while frontier:
        y, x = frontier.pop()
        for y_diff, x_diff in NEIGHBOR_DIFFS:
            y2 = y + y_diff
            x2 = x + x_diff
            if x2 >= 0 and y2 >= 0 and x2 < WIDTH and y2 < HEIGHT \
                    and height_map[y2][x2] != MAX_HEIGHT \
                    and (y2, x2) not in visited:
                visited.add((y2, x2))
                frontier.append((y2, x2))
    basin_sizes.append(len(visited))

three_largest = sorted(basin_sizes, reverse=True)[0:3]
print(three_largest[0] * three_largest[1] * three_largest[2])