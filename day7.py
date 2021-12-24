# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 22:56:41 2021

@author: Q
"""

def count_fuel_to_target_position(count_buckets, target):
    return sum([abs(start_pos - target) * count for start_pos, count in count_buckets.items()])

with open('day7.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

input_nums = [int(x) for x in lines[0].split(',')]
count_buckets = {}
for num in input_nums:
    if num not in count_buckets:
        count_buckets[num] = 0
    count_buckets[num] += 1
jump_buckets = list(count_buckets.items())
jump_buckets.sort()
# convert each tuple (a,b) into a list [a,b]
jump_buckets = [[a, b] for (a, b) in jump_buckets]

while len(jump_buckets) > 1:
    # print(jump_buckets)
    if jump_buckets[0][1] < jump_buckets[-1][1]:
        # less of lowest position than of highest
        # move them all to next populated position (higher)
        jump_buckets[1][1] += jump_buckets[0][1]
        jump_buckets = jump_buckets[1:]
    else: # jump_buckets[0][1] >= jump_buckets[-1][1]:
        # less of highest position than of lowest
        # move them all to next populated position (lower)
        jump_buckets[-2][1] += jump_buckets[-1][1]
        jump_buckets = jump_buckets[:-1]

best_target_position = jump_buckets[0][0]
fuel = count_fuel_to_target_position(count_buckets, best_target_position)
# print(best_target_position-1, count_fuel_to_target_position(count_buckets, best_target_position-1))
# print(best_target_position, fuel, '(best solution)')
# print(best_target_position+1, count_fuel_to_target_position(count_buckets, best_target_position+1))

print(fuel)


########

# part 2 requires binary searching

def fuel_cost_of_distance(n):
    # = sum_range_to_n
    return (n * (n + 1)) // 2

def count_fuel_to_target_position_part_2(count_buckets, target):
    return sum([fuel_cost_of_distance(abs(start_pos - target)) * count for start_pos, count in count_buckets.items()])

# binary search time!
low = min(count_buckets.keys())
high = max(count_buckets.keys())
while low != high:
    fuel_if_low_is_target = count_fuel_to_target_position_part_2(count_buckets, low)
    fuel_if_high_is_target = count_fuel_to_target_position_part_2(count_buckets, high)
    print(low, fuel_if_low_is_target, 'vs', high, fuel_if_high_is_target)
    if fuel_if_low_is_target < fuel_if_high_is_target:
        high = (low + high) // 2
    elif fuel_if_low_is_target > fuel_if_high_is_target:
        if low == high - 1:
            low = high
        low = (low + high) // 2
    else:
        low = high

best_target_position = low
fuel = count_fuel_to_target_position_part_2(count_buckets, best_target_position)
# print(best_target_position-1, count_fuel_to_target_position_part_2(count_buckets, best_target_position-1))
# print(best_target_position, fuel, '(best solution)')
# print(best_target_position+1, count_fuel_to_target_position_part_2(count_buckets, best_target_position+1))

print(fuel)
