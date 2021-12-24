# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 19:18:50 2021

@author: Q
"""

with open('day2.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

depth = 0
distance = 0

for line in lines:
   command, valuestr = line.split(" ")
   value = int(valuestr)
   if command == "forward":
       distance += value
   elif command == "up":
       depth -= value
   elif command == "down":
       depth += value
   else:
       print("booooo!", line)
       
total = depth * distance

print(total)  # 2150351


#####################


depth = 0
distance = 0
aim = 0

for line in lines:
   command, valuestr = line.split(" ")
   value = int(valuestr)
   if command == "forward":
       distance += value
       depth += aim * value
   elif command == "up":
       aim -= value
   elif command == "down":
       aim += value
   else:
       print("booooo!", line)
       
total = depth * distance

print(total)  # 1842742223