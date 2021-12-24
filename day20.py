with open('day20.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

algorithm_map = [1 if c == '#' else 0 for c in lines[0]]
pixels = {}
WIDTH = len(lines[2])
HEIGHT = len(lines) - 2
EXTRA = 5
y_counter = -1
for y in range(HEIGHT):
    for x in range(WIDTH):
        pixels[(x, y)] = 1 if lines[2 + y][x] == '#' else 0

output = {}
for step in range(2):
    output = {}
    base_pixel = 0 if algorithm_map[0] == 0 else step % 2
    for x in range(0 - step - EXTRA, WIDTH + step + EXTRA):
        for y in range(0 - step - EXTRA, HEIGHT + step + EXTRA):
            total = 0
            for yy in range(y - 1, y + 2):
                for xx in range(x - 1, x + 2):
                    total = total * 2 + pixels.get((xx, yy), base_pixel)
            output[(x, y)] = algorithm_map[total]
    # print()
    # for y in range(0 - step - EXTRA, HEIGHT + step + EXTRA):
    #     for x in range(0 - step - EXTRA, WIDTH + step + EXTRA):
    #         print('#' if output[(x, y)] else '.', end='')
    #     print()
    pixels = output

print(sum(output.values()))  # 5663

for step in range(50 - 2):
    output = {}
    base_pixel = 0 if algorithm_map[0] == 0 else step % 2
    for x in range(0 - step - EXTRA, WIDTH + step + EXTRA):
        for y in range(0 - step - EXTRA, HEIGHT + step + EXTRA):
            total = 0
            for yy in range(y - 1, y + 2):
                for xx in range(x - 1, x + 2):
                    total = total * 2 + pixels.get((xx, yy), base_pixel)
            output[(x, y)] = algorithm_map[total]
    pixels = output

print(sum(output.values()))  # 19638