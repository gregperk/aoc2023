#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=['example0.txt', 'input.txt'])
width = len(lines[0])
height = len(lines)

galaxies = [(x,y) for x in range(width) for y in range(height) if lines[y][x] == '#']

free_rows = [idx for idx,line in enumerate(lines) if all(x == '.' for x in line)]

free_cols = reduce(lambda result, line: [result[i] and line[i]=='.' for i in range(width)],lines, [True]*width)
free_cols = [idx for idx,val in enumerate(free_cols) if val]

expansions = lambda a, b, vals: len([x for x in vals if x > min(a,b) and x < max(a,b)])

def distance(a, b, expansion_factor):
    ax,ay = a
    bx,by = b

    dx = abs(ax - bx)
    dy = abs(ay - by)
    ex = (expansion_factor - 1) * expansions(ax, bx, free_cols)
    ey = (expansion_factor - 1) * expansions(ay, by, free_rows)

    return dx + dy + ex + ey

print(sum(distance(a, b, 2) for a,b in combinations(galaxies, 2)))
