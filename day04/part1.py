#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])

points = 0
for line in lines:
    winners, holding = line.split(":")[1].split("|")
    n_matching = len(set(winners.split()) & set(holding.split()))
    if n_matching > 0:
        points += pow(2, n_matching - 1)

print(points)
