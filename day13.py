with open('day13.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

points = []
folds = []
for line in lines:
    if ',' in line:
        x, y = [int(n) for n in line.split(',')]
        points.append((x, y))
    elif 'fold' in line:
        equals_index = line.index('=')
        fold = (line[equals_index - 1], int(line[equals_index + 1:]))
        folds.append(fold)


def print_points():
    for y in range(max(y2 for x2, y2 in points) + 1):
        for x in range(max(x2 for x2, y2 in points) + 1):
            print('█' if (x, y) in points else '.', end='')
        print()


# print_points()

step = 0
for fold in folds:
    step += 1
    axis, offset = fold
    if axis == 'x':
        points = [(x if x < offset else 2 * offset - x, y) for (x, y) in points]
    elif axis == 'y':
        points = [(x, y if y < offset else 2 * offset - y) for (x, y) in points]
    points = list(set(points))
    if step == 1:
        print(len(points))

print_points()
