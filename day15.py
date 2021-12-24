from heapq import heapify, heappop, heappush

with open('day15.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]
HEIGHT = len(lines)
WIDTH = len(lines[0])
# print(WIDTH, HEIGHT)
cavern = {}
for y in range(HEIGHT):
    for x in range(WIDTH):
        cavern[(x, y)] = int(lines[y][x])

risk_until = {}
heap = [(0, 0, 0)]
risk_until[(0, 0)] = 0  # NOT cavern[(0, 0)]
while heap:
    point = heappop(heap)
    risk_until_point, x, y = point
    for neighbor in [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1),
    ]:
        x2, y2 = neighbor
        if x2 < 0 or y2 < 0 or x2 > WIDTH-1 or y2 > HEIGHT-1:
            continue
        risk_until_neighbor = risk_until_point + cavern[neighbor]
        if neighbor not in risk_until:
            risk_until[neighbor] = risk_until_neighbor
            heappush(heap, (risk_until_neighbor, x2, y2))
        else:
            risk_until[neighbor] = min(risk_until[neighbor], risk_until_neighbor)


print(risk_until[(WIDTH-1, HEIGHT-1)])  # 698


BIG_WIDTH = WIDTH * 5
BIG_HEIGHT = HEIGHT * 5
risk_until = {}
heap = [(0, 0, 0)]
risk_until[(0, 0)] = 0  # NOT cavern[(0, 0)]
while heap:
    point = heappop(heap)
    risk_until_point, x, y = point
    for neighbor in [
        (x-1, y),
        (x+1, y),
        (x, y-1),
        (x, y+1),
    ]:
        x2, y2 = neighbor
        if x2 < 0 or y2 < 0 or x2 > BIG_WIDTH-1 or y2 > BIG_HEIGHT-1:
            continue
        risk_of_neighbor = cavern[x2 % WIDTH, y2 % HEIGHT] + (x2 // WIDTH) + (y2 // HEIGHT)
        if risk_of_neighbor > 9:
            risk_of_neighbor -= 9
        risk_until_neighbor = risk_until_point + risk_of_neighbor
        if neighbor not in risk_until:
            risk_until[neighbor] = risk_until_neighbor
            heappush(heap, (risk_until_neighbor, x2, y2))
        else:
            risk_until[neighbor] = min(risk_until[neighbor], risk_until_neighbor)


print(risk_until[(BIG_WIDTH-1, BIG_HEIGHT-1)])  #
