import heapq

with open('day21.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

players = [
    # index, position (0-9), score (0-1000+)
    (int(lines[0][-1]) - 1, 0),
    (int(lines[1][-1]) - 1, 0)
]
THOUSAND = 1000
TEN = 10

rolls = 0
turn = 0
while all(p[1] < THOUSAND for p in players):
    player_idx = 0 if turn % 2 == 0 else 1
    player_position, player_score = players[player_idx]
    next_position = (player_position + (rolls * 3) + 6) % TEN
    players[player_idx] = (next_position, player_score + next_position + 1)
    rolls += 3
    turn += 1

loser = players[0] if players[0][1] < 1000 else players[1]
print(loser[1] * rolls)  # 513936

# part 2

universe_counts = {}
# each universe is a tuple, with data in such a way that universes are always sorted "chronologically"
first_universe = (
    # lowest score
    # highest score
    # whose turn is it?
    # player 0 position
    # player 0 score
    # player 1 position
    # player 1 score
    0,
    0,
    0,
    int(lines[0][-1]) - 1,
    0,
    int(lines[1][-1]) - 1,
    0,
)
THREE_D_THREE_RESULTS = [
    # roll, occurrences
    (3, 1),
    (4, 3),
    (5, 6),
    (6, 7),
    (7, 6),
    (8, 3),
    (9, 1),
]
TWENTY_ONE = 21
universe_counts[first_universe] = 1
uncalculated_universes = [first_universe]
total_wins = [0, 0]
while uncalculated_universes:
    universe = heapq.heappop(uncalculated_universes)
    lowest_score, highest_score, turn, p0_pos, p0_score, p1_pos, p1_score = universe
    # roll will be 1, 2, or 3
    for roll, occurrences in THREE_D_THREE_RESULTS:
        universe_count = universe_counts[universe] * occurrences
        p0_turn = turn % 2 == 0
        prev_position = p0_pos if p0_turn else p1_pos
        next_position = (prev_position + roll) % TEN
        prev_score = p0_score if p0_turn else p1_score
        next_score = prev_score + next_position + 1
        if next_score >= TWENTY_ONE:
            total_wins[turn % 2] += universe_count
            continue
        if p0_turn:
            new_universe = (
                min(next_score, p1_score),
                max(next_score, p1_score),
                turn + 1,
                next_position,
                next_score,
                p1_pos,
                p1_score
            )
        else:  # was p1 turn
            new_universe = (
                min(next_score, p0_score),
                max(next_score, p0_score),
                turn + 1,
                p0_pos,
                p0_score,
                next_position,
                next_score
            )
        if new_universe not in universe_counts:
            heapq.heappush(uncalculated_universes, new_universe)
            universe_counts[new_universe] = 0
        universe_counts[new_universe] += universe_count

print(max(total_wins))  # 105619718613031