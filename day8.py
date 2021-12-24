# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 23:02:37 2021

@author: Q
"""

with open('day8.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

def is_one_of_1478(abcdefg):
    return len(abcdefg) in [2, 4, 3, 7]

parsed_lines = []
for line in lines:
    start, end = line.split(' | ')
    parsed_lines.append([start.split(' '), end.split(' ')])
    
answer = sum(sum(1 if is_one_of_1478(abcdefg) else 0 for abcdefg in line[1]) for line in parsed_lines)
print(answer)

# deductive solution time

SEGMENTS = {
    'ABCEFG': 0,
    'CF': 1,
    'ACDEG': 2,
    'ACDFG': 3,
    'BCDF': 4,
    'ABDFG': 5,
    'ABDEFG': 6,
    'ACF': 7,
    'ABCDEFG': 8,
    'ABCDFG': 9,
}

def decode(unsorted_pattern, configuration):
    segment_indices = [configuration.index(c) for c in unsorted_pattern]
    segment_letters = [chr(ord('A') + i) for i in segment_indices]
    return str(SEGMENTS[''.join(sorted(segment_letters))])
    

answer_total = 0
for line in parsed_lines:
    patterns = line[0]
    one = next(p for p in patterns if len(p) == 2)
    four = next(p for p in patterns if len(p) == 4)
    seven = next(p for p in patterns if len(p) == 3)
    eight = next(p for p in patterns if len(p) == 7)
    # the segment at the top (A) is the one that seven includes and one does not.
    A = next(c for c in seven if c not in one)
    nine = next(p for p in patterns if len(p) == 6 \
                and all(c in p for c in four)\
                and A in p)
    G = next(c for c in nine if c not in four and c is not A)
    E = next(c for c in eight if c not in nine)
    zero = next(p for p in patterns if len(p) == 6 \
                and all(c in p for c in one)\
                and A in p and E in p and G in p)
    B = next(c for c in zero if c not in one and c not in [A, G, E]) 
    three = next(p for p in patterns if len(p) == 5 \
                and all(c in p for c in one)\
                and A in p and G in p)
    D = next(c for c in three if c not in one and c not in [A, G]) 
    two = next(p for p in patterns if len(p) == 5 \
                and all(c in p for c in [A, D, E, G]))
    C = next(c for c in two if c not in [A, D, E, G])
    F = next(c for c in one if c is not C)
    configuration = [A, B, C, D, E, F, G]
    output_patterns = line[1]
    output_digits = ''.join(decode(x, configuration) for x in output_patterns)
    output_value = int(output_digits)
    answer_total += output_value

print(answer_total)