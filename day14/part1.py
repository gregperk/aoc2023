#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 136), ('input.txt', 108813)])

grid = [list(line) for line in case_lines()]
height = len(grid)
width = len(grid[0])

def tilt_north():
    rest = height + 1
    for x in range(width):
        for y in range(height):
            if grid[y][x] == 'O' and rest >= y:
                rest = y+1
            if grid[y][x] == '.' and rest > y:
                rest = y
            elif grid[y][x] == 'O' and rest < y:
                grid[y][x] = '.'
                grid[rest][x] = 'O'
                rest += 1
            elif grid[y][x] == '#':
                rest = y+1

def calculate_load():
    return sum(height-y for x in range(width) for y in range(height) if grid[y][x]=='O')

tilt_north()
load = calculate_load()

assert_solution(load)
