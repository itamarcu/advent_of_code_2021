# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 22:26:37 2021

@author: Q
"""

with open('day6.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

fishies = [int(number) for number in lines[0].split(',')]

fishie_clusters = [0] * 9

for fish in fishies:
    fishie_clusters[fish] += 1
    
for day in range(256):
    newborns = fishie_clusters[0]
    fishie_clusters = fishie_clusters[1:] + [newborns]
    fishie_clusters[6] += newborns
    
total = sum(fishie_clusters)

print(total)
