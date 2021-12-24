with open('day11.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

octopuses = [[int(c) for c in line] for line in lines]

ADJACENCY_DIFFS = [
    (-1, -1), (-1, 0), (-1, +1),
    (0, -1), (0, 0), (0, +1),
    (+1, -1), (+1, 0), (+1, +1),
]

total_flashes = 0
step = -1
while True:
    step += 1
    # increase all by 1
    octopuses = [[o + 1 for o in line] for line in octopuses]
    # flash all who reach 10+
    while any(any(10 <= o <= 99 for o in line) for line in octopuses):
        for y in range(len(octopuses)):
            for x in range(len(octopuses[0])):
                if 10 <= octopuses[y][x] <= 99:
                    for diff_y, diff_x in ADJACENCY_DIFFS:
                        x2 = x + diff_x
                        y2 = y + diff_y
                        if 0 <= y2 <= len(octopuses) - 1 and 0 <= x2 <= len(octopuses[0]) - 1:
                            octopuses[y2][x2] += 1
                    octopuses[y][x] = 999
    # count flashes
    flashes_this_step = sum(sum(o >= 10 for o in line) for line in octopuses)
    # print them all
    print(f'step {step}: {flashes_this_step}')
    for line in octopuses:
        print(''.join(str(o if o < 10 else '█') for o in line))
    print()
    total_flashes += flashes_this_step
    # reset flashes
    octopuses = [[0 if o >= 10 else o for o in line] for line in octopuses]
    # part 1
    if step == 100:
        print(total_flashes)  # 1721
    if flashes_this_step == len(octopuses) * len(octopuses[0]):
        print(step + 1)  #
        break
