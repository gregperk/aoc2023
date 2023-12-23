#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 94), ('input.txt', 2358)])

sys.setrecursionlimit(5000)

grid = [list(line) for line in case_lines()]
height = len(grid)
width = len(grid[0])

slopes = {
    '>': (+1,0),
    '<': (-1,0),
    'v': (0,+1),
    '^': (0,-1)
}

def delta(from_loc,to_loc):
    fx,fy = from_loc
    tx,ty = to_loc
    return (tx-fx,ty-fy)

def moves(loc):
    x,y = loc
    basic = [(x+dx,y+dy) for dx in [-1,0,+1] for dy in [-1,0,+1] if abs(dx)!=abs(dy)]
    in_bounds = [(x,y) for x,y in basic if x>=0 and x<width and y>=0 and y<height]
    on_path = [(x,y) for x,y in in_bounds if grid[y][x]=='.' or (grid[y][x] in slopes.keys() and slopes[grid[y][x]]==delta(loc,(x,y)))]
    return set(on_path)

def longest_between(start_loc, end_loc, path_elements):
    current = path_elements | {start_loc}

    if end_loc in current:
        return current

    longest = set()
    for m in moves(start_loc) - path_elements:
        option = longest_between(m, end_loc, current)
        if len(option) > len(longest):
            longest = option;

    return longest

def grid_str():
    return '\n'.join(''.join(x for x in row) for row in grid)

print(grid_str())

path_elements = longest_between((1,0), (width-2,height-1), set())
for x,y in path_elements:
    grid[y][x] = 'O'

print('\n'+grid_str())

assert_solution(len(path_elements)-1)
    