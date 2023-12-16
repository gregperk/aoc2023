#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 46), ('input.txt', 7979)])

grid = [line for line in case_lines()]
height = len(grid)
width = len(grid[0])

def step(loc, dir):
    x,y = loc
    dx,dy = dir
    return (x+dx, y+dy)

def in_bounds(loc):
    x,y = loc
    return x>=0 and x<width and y>=0 and y<height

optics = {
    ('.', (0,-1)): [(0,-1)],
    ('.', (+1,0)): [(+1,0)],
    ('.', (0,+1)): [(0,+1)],
    ('.', (-1,0)): [(-1,0)],

    ('/', (0,-1)): [(+1,0)],
    ('/', (+1,0)): [(0,-1)],
    ('/', (0,+1)): [(-1,0)],
    ('/', (-1,0)): [(0,+1)],

    ('\\', (0,-1)): [(-1,0)],
    ('\\', (+1,0)): [(0,+1)],
    ('\\', (0,+1)): [(+1,0)],
    ('\\', (-1,0)): [(0,-1)],

    ('-', (0,-1)): [(-1,0),(+1,0)],
    ('-', (+1,0)): [(+1,0)],
    ('-', (0,+1)): [(-1,0),(+1,0)],
    ('-', (-1,0)): [(-1,0)],

    ('|', (0,-1)): [(0,-1)],
    ('|', (+1,0)): [(0,-1),(0,+1)],
    ('|', (0,+1)): [(0,+1)],
    ('|', (-1,0)): [(0,-1),(0,+1)],
}

def trace(first_loc, first_dir):
    notes = defaultdict(lambda: set())

    queue = deque([(first_loc, first_dir)])
    while queue:
        loc,dir = queue.popleft()
        x,y = loc

        if dir not in notes[loc]:
            notes[loc].add(dir)
            for next_dir in optics[(grid[y][x], dir)]:
                next_loc = step(loc, next_dir)
                if in_bounds(next_loc):
                    queue.append((next_loc, next_dir))

    return sum(1 if notes[(x,y)] else 0 for x in range(width) for y in range(height))


assert_solution(trace((0,0),(1,0)))
