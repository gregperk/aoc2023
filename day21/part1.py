#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 42), ('input.txt', 3666)])

grid = [list(line) for line in case_lines()]
height = len(grid)
width = len(grid[0])
start = next((x,y) for x in range(width) for y in range(height) if grid[y][x]=='S')

def neighbors(loc):
    x,y = loc
    locs = [(x+dx,y+dy) for dx,dy in [(-1,0),(+1,0),(0,-1),(0,+1)]]
    locs = [(x,y) for x,y in locs if x>=0 and x<width and y>=0 and y<height and grid[y][x]!='#']
    return locs

def step(curr):
    next = set()
    for c in curr:
        next.update(neighbors(c))
    return next

def solve(n):
    curr = set([start])
    for _ in range(n):
        curr = step(curr)
    
    return len(curr)

assert_solution(solve(64))
