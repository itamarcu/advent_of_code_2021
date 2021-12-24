# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 00:12:47 2021

@author: Q
"""

with open('day5.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

points_seen_counts = {}  # e.g. (0, 0): 0
for line in lines:
    start, end = line.split(' -> ')
    x1, y1 = [int(k) for k in start.split(',')]
    x2, y2 = [int(k) for k in end.split(',')]
    if x1 == x2:
        # vertical
        for y in range(min(y1,y2), max(y1,y2) + 1):
            point = (x1, y)
            if point not in points_seen_counts:
                points_seen_counts[point] = 0
            points_seen_counts[point] += 1
    elif y1 == y2:
        # horizontal
        for x in range(min(x1,x2), max(x1,x2) + 1):
            point = (x, y1)
            if point not in points_seen_counts:
                points_seen_counts[point] = 0
            points_seen_counts[point] += 1
    else:
        # diagonal
        continue
        
for y in range(10):
    print(''.join(str(points_seen_counts.get((x, y), '.')) for x in range(10)))

total = 0
for point, count in points_seen_counts.items():
    if count >= 2:
        total += 1
        
print(total)


for line in lines:
    start, end = line.split(' -> ')
    x1, y1 = [int(k) for k in start.split(',')]
    x2, y2 = [int(k) for k in end.split(',')]
    if x1 == x2:
        # vertical
        pass
    elif y1 == y2:
        # horizontal
        pass
    else:
        # diagonal
        line_length = abs(x2 - x1)
        direction_x = (x2 - x1) / line_length
        direction_y = (y2 - y1) / line_length
        for i in range(line_length + 1):
            point = (x1 + direction_x * i, y1 + direction_y * i)
            if point not in points_seen_counts:
                points_seen_counts[point] = 0
            points_seen_counts[point] += 1

total = 0
for point, count in points_seen_counts.items():
    if count >= 2:
        total += 1
        
for y in range(10):
    print(''.join(str(points_seen_counts.get((x, y), '.')) for x in range(10)))
    
print(total)