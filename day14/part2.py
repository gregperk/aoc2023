#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 64), ('input.txt', 104533)])

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

def spin_once():
    global grid
    for _ in range(4):
        tilt_north()
        grid = [
            [grid[y][x] for y in range(len(grid) - 1, -1, -1)]
            for x in range(len(grid[0]))
        ]

def discover_load_cycle():
    memo = dict()
    for spin_num in count():
        spin_once()
        snapshot = "".join("".join(row) for row in grid)
        if snapshot in memo:
            if memo[snapshot]:
                return sorted([v for v in memo.values() if v])
            memo[snapshot] = (spin_num, calculate_load())
        else:
            memo[snapshot] = None

cycle = discover_load_cycle()
load = cycle[(1_000_000_000 - cycle[0][0] - 1) % len(cycle)][1]

assert_solution(load)
