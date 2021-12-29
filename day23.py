import json
from typing import Optional, List, Tuple

LETTER_TO_INDEX = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
}
INDEX_TO_LETTER = {
    0: 'A',
    1: 'B',
    2: 'C',
    3: 'D',
}
LETTER_TO_COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000,
}
ROOM_XS = [3, 5, 7, 9]
HALLWAY_MIN_X = 1
HALLWAY_MAX_X = 11


def main():
    with open('day23.txt') as input_file:
        input_lines = input_file.readlines()
    lines = [line.rstrip('\n') for line in input_lines]

    # input format:
    # #############
    # #...........#
    # ###B#C#B#D###
    #   #A#D#C#A#
    #   #########
    hallway: Hallway = ['#' if c == '#' else None for c in lines[1]]
    # ugly but oh well
    rooms: Rooms = [
        [lines[2][3], lines[3][3]],
        [lines[2][5], lines[3][5]],
        [lines[2][7], lines[3][7]],
        [lines[2][9], lines[3][9]],
    ]

    state = (0, hallway, rooms)
    print(solve_part(1, state))  # 15237

    # adding:
    #   #D#C#B#A#
    #   #D#B#A#C#
    rooms: Rooms = [
        [lines[2][3], 'D', 'D', lines[3][3]],
        [lines[2][5], 'C', 'B', lines[3][5]],
        [lines[2][7], 'B', 'A', lines[3][7]],
        [lines[2][9], 'A', 'C', lines[3][9]],
    ]
    state = (0, hallway, rooms)
    static['min_solution_cost_seen'] = 99999999999999999999
    static['states_checked'] = set()
    print(solve_part(2, state))  # 47509


Cost = int
Hallway = List[Optional[str]]
Rooms = List[List[Optional[str]]]
State = Tuple[Cost, Hallway, Rooms]  # hallway, rooms

static = {
    'min_solution_cost_seen': 99999999999999999999,
    'states_checked': set(),
}


def solve_part(part: int, state: State) -> Optional[Cost]:
    depths = 2 if part == 1 else 4
    cost, hallway, rooms = state
    dumps = json.dumps(state)
    if dumps in static['states_checked']:
        return None
    static['states_checked'].add(dumps)
    # if len(static['states_checked']) % 100000 == 0:
    #     print('#', len(static['states_checked']))
    # check if we finished
    goal = 'AABBCCDD' if part == 1 else 'AAAABBBBCCCCDDDD'
    if ''.join(''.join(c or '.' for c in room) for room in rooms) == goal:
        static['min_solution_cost_seen'] = min(cost, static['min_solution_cost_seen'])
        # print('FOUND', cost)
        return cost
    # list various moves
    possible_next_states = []
    # 1. try moving from hallway to correct room
    for x, c in enumerate(hallway):
        if c is None or c == '#':
            continue
        # identify where it should go
        target_room_i = LETTER_TO_INDEX[c]
        target_room_x = ROOM_XS[target_room_i]
        target_room = rooms[target_room_i]
        # make sure target room is valid
        if any(c2 != c and c2 is not None for c2 in target_room):
            continue
        # make sure path is clear
        if x < target_room_x:
            if any(c is not None for c in hallway[x + 1: target_room_x + 1]):
                continue
        else:
            if any(c is not None for c in hallway[target_room_x: x]):
                continue
        # all good!
        distance = abs(target_room_x - x) + 1
        new_target_room = target_room.copy()
        # target_room[1] is the deeper/bottom space in the target room, it's the stuff at lines[3]
        target_depth = max(i for i in range(depths) if target_room[i] is None)
        distance += target_depth
        new_target_room[target_depth] = c
        new_cost = cost + distance * LETTER_TO_COST[c]
        if new_cost >= static['min_solution_cost_seen']:
            continue
        new_hallway = hallway.copy()
        new_hallway[x] = None
        new_rooms = rooms.copy()
        new_rooms[target_room_i] = new_target_room
        possible_next_states.append((new_cost, new_hallway, new_rooms))
    # 2. try moving from room to hallway
    for room_i in range(4):
        room = rooms[room_i]
        correct_letter = INDEX_TO_LETTER[room_i]
        if all(c2 == correct_letter or c2 is None for c2 in room):
            # this room is already correct
            continue
        room_x = ROOM_XS[room_i]
        for depth_i in range(depths):
            c = room[depth_i]
            if c is None:
                continue
            if any(r is not None for r in room[0:depth_i]):
                # stuck under others above it
                continue
            left_obstacle_x = next(x for x in range(room_x, HALLWAY_MIN_X - 2, -1) if hallway[x] is not None)
            right_obstacle_x = next(x for x in range(room_x, HALLWAY_MAX_X + 2, +1) if hallway[x] is not None)
            valid_xs = [x for x in range(left_obstacle_x + 1, right_obstacle_x) if x not in ROOM_XS]
            for x in valid_xs:
                # all good!
                distance = abs(room_x - x) + 1 + depth_i
                new_room = room.copy()
                new_room[depth_i] = None
                new_cost = cost + distance * LETTER_TO_COST[c]
                if new_cost >= static['min_solution_cost_seen']:
                    continue
                new_hallway = hallway.copy()
                new_hallway[x] = c
                new_rooms = rooms.copy()
                new_rooms[room_i] = new_room
                possible_next_states.append((new_cost, new_hallway, new_rooms))
    # sort cheapest first
    possible_next_states.sort(key=lambda s: s[0])
    solution_costs = [solve_part(part, s) for s in possible_next_states]
    solution_costs = [c for c in solution_costs if c is not None]
    if len(solution_costs) == 0:
        # no solution found
        return None
    return min(solution_costs)


def visual_state(state: State) -> str:
    # #############
    # #...........#
    # ###B#C#B#D###
    #   #A#D#C#A#
    #   #########
    # ->
    # #...........# | BA CD BC DA
    _, hallway, rooms = state
    return ''.join(c or '.' for c in hallway) + ' | ' + ' '.join(''.join(c or '.' for c in room) for room in rooms)


if __name__ == '__main__':
    main()
