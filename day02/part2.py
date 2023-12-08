#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])

power_sum = 0

for line in lines:
    [game, rest] = line.split(":")

    draws = rest.split(";")
    maxes = defaultdict(int)
    for draw in draws:
        colors = draw.split(",")
        for color in colors:
            [count, label] = color.strip().split()
            maxes[label] = max(maxes[label], int(count))

    power_sum += reduce(mul, maxes.values(), 1)

print(power_sum)
