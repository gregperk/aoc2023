#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])
times = [int(s) for s in lines[0].split(":")[1].split()]
distances = [int(s) for s in lines[1].split(":")[1].split()]
time_distances = zip(times, distances)

wins = lambda time, dist: [t for t in range(time + 1) if t * (time - t) > dist]
answer = reduce(mul, [len(wins(time, dist)) for time, dist in time_distances], 1)

print(answer)
