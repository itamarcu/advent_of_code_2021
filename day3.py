# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 22:51:23 2021

@author: Q
"""

with open('day3.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

line_count = len(lines)
digit_count = len(lines[0])
counters = [0] * digit_count

for line in lines:
     for i in range(digit_count):
         counters[i] += int(line[i])

gammas = [0] * digit_count
epsilons = [0] * digit_count
for i in range(digit_count):
    gammas[i] = '1' if counters[i] / line_count > 0.5 else '0'
    epsilons[i] = '0' if counters[i] / line_count > 0.5 else '1'

gamma = int(''.join(gammas), 2)
epsilon = int(''.join(epsilons), 2)
print(gamma * epsilon)  # 2967914

#########################


def filtered_numbers_by_common_at_i(numbers, i, least_common):
    counter = sum([int(number[i]) for number in numbers])
    common = '1' if counter >= len(numbers) / 2 else '0'
    if len(numbers) == 1:
        return numbers
    return [num for num in numbers if (num[i] == common) != least_common]


leftover_numbers = lines
for i in range(digit_count):
    leftover_numbers = filtered_numbers_by_common_at_i(leftover_numbers, i, False)
oxygen_generator_rating = leftover_numbers[0]
leftover_numbers = lines
for i in range(digit_count):
    leftover_numbers = filtered_numbers_by_common_at_i(leftover_numbers, i, True)
co2_scrubber_rating = leftover_numbers[0]

oxygen_generator_rating = int(''.join(oxygen_generator_rating), 2)
co2_scrubber_rating = int(''.join(co2_scrubber_rating), 2)
print(oxygen_generator_rating * co2_scrubber_rating)  # 7041258
