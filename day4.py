# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 21:21:43 2021

@author: Q
"""


def mark_number_in_board(board, number):
    for x in range(5):
        for y in range(5):
            if board[x][y] == number:
                board[x][y] = None
                return True
    return False

def check_if_line_won(board, x):
    for y in range(5):
        if board[x][y] is not None:
            return False
    return True

def check_if_column_won(board, y):
    for x in range(5):
        if board[x][y] is not None:
            return False
    return True

def check_if_dexter_diagonal_won(board):
    for x in range(5):
        if board[x][x] is not None:
            return False
    return True

def check_if_sinister_diagonal_won(board):
    for x in range(5):
        if board[x][4-x] is not None:
            return False
    return True

def check_if_board_won(board):
    for x in range(5):
        if (check_if_line_won(board, x)):
            return True
    for y in range(5):
        if (check_if_column_won(board, y)):
            return True
    #if (check_if_dexter_diagonal_won(board)):
    #    return True
    #if (check_if_sinister_diagonal_won(board)):
    #    return True
    return False
    
def calculate_score(board, number):
    total_sum = 0
    for x in range(5):
        for y in range(5):
            if board[x][y] is not None:
                total_sum += board[x][y]
    return total_sum * number

        

with open('day4.txt') as input_file:
    input_lines = input_file.readlines()
lines = [line.rstrip('\n') for line in input_lines]

def setup(lines):
    called_numbers = [int(number) for number in lines[0].split(',')]
    boards = []
    for i in range(1, len(lines)):
        if lines[i] == "":
            current_board = [[None for x in range(5)] for y in range(5)]
            j = 0
            boards.append(current_board)
        else:
            line_numbers = [int(number) for number in lines[i].split(' ') if number != '']
            current_board[j] = line_numbers
            j += 1
    return (boards, called_numbers)

def run_bingo_until_win(boards, called_numbers):
    for number in called_numbers:
        for board in boards:
            found = mark_number_in_board(board, number)
            if found:
                bingo = check_if_board_won(board)
                if bingo:
                    score = calculate_score(board, number)
                    return score
                
boards, called_numbers = setup(lines)
print(run_bingo_until_win(boards, called_numbers))  # 33462
                    
                    
##################


def run_bingo_until_last_win(boards, called_numbers):
    boards_left = len(boards)
    for number in called_numbers:
        for board in boards:
            if (check_if_board_won(board)):
                continue
            found = mark_number_in_board(board, number)
            if found:
                bingo = check_if_board_won(board)
                if bingo:
                    boards_left -= 1
                    if boards_left == 0:
                        score = calculate_score(board, number)
                        return score
                

boards, called_numbers = setup(lines)
print(run_bingo_until_last_win(boards, called_numbers)) # 30070



#i = 0
#for board in boards:
#    print('board', i)
#    i += 1
#    for line in board:
#        print(line)
#print(boards)
#current_board[2][3] = 7
#print(current_board)