# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:18:50 2021

@author: Q
"""

with open('day1-submarine-input.txt') as input_file:
    input_lines = input_file.readlines()
depths = [int(line.rstrip('\n')) for line in input_lines]
    
increases = 0

for i in range(len(depths)-1):
    depth_1 = depths[i]
    depth_2 = depths[i+1]
    if depth_2 > depth_1:
        increases += 1

print(increases)


window_increases = 0

for i in range(len(depths)-3):
    depth_1 = depths[i]
    depth_4 = depths[i+3]
    if depth_4  > depth_1:
        window_increases += 1

print(window_increases)