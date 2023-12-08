#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])

maximum = {"red": 12, "green": 13, "blue": 14}

success_sum = 0
for line in lines:
    [game, rest] = line.split(":")

    game_number = int(game.split()[1])

    draws = rest.split(";")
    overdrawn = False
    for draw in draws:
        colors = draw.split(",")
        for color in colors:
            [count, label] = color.strip().split()
            if int(count) > maximum[label]:
                overdrawn = True

    success_sum += 0 if overdrawn else game_number

print(success_sum)
