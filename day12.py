from typing import List, Dict


class Cave:
    name: str
    is_big: bool
    neighbors: List[str]

    def __init__(self, name: str):
        self.name = name
        self.is_big = name[0].isupper()
        self.neighbors = []


Path = List[str]  # list of cave names
START = 'start'
END = 'end'
START_MARKED = 'start__also_we_repeated_once'

with open('day12.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]


caves: Dict[str, Cave] = {}
for line in lines:
    c_from, c_to = line.split('-')
    if c_from not in caves:
        caves[c_from] = Cave(c_from)
    if c_to not in caves:
        caves[c_to] = Cave(c_to)
    caves[c_from].neighbors.append(c_to)
    caves[c_to].neighbors.append(c_from)

complete_paths: List[Path] = []
paths: List[Path] = [[START]]
while paths:
    path = paths.pop(0)
    latest_cave = caves[path[-1]]
    for neighbor_cave in latest_cave.neighbors:
        if neighbor_cave == END:
            complete_paths.append(path + ['end'])
            continue
        if neighbor_cave in path and not caves[neighbor_cave].is_big:
            continue
        paths.append(path + [neighbor_cave])

print(len(complete_paths))  # 5333

# (the next part takes some time to calculate)

complete_paths: List[Path] = []
paths: List[Path] = [[START]]
while paths:
    path = paths.pop(0)
    latest_cave = caves[path[-1]]
    for neighbor_cave in latest_cave.neighbors:
        new_path = path.copy()
        if neighbor_cave == END:
            new_path.append('end')
            complete_paths.append(new_path)
            continue
        if neighbor_cave == START:
            continue
        if neighbor_cave in new_path and not caves[neighbor_cave].is_big:
            # allow but only once per path
            # hacky way: mark that we did it this path in the first path node name
            if new_path[0] == START_MARKED:
                continue
            else:
                new_path[0] = START_MARKED
        new_path.append(neighbor_cave)
        paths.append(new_path)

# for path in complete_paths:
#     print(','.join(path))
print(len(complete_paths))  # 146553
