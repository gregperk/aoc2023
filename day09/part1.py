#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])
histories = [list(map(int, line.split())) for line in lines]

diffs = lambda seq: [seq[i] - seq[i-1] for i in range(1, len(seq))]
zeros = lambda seq: all(x == 0 for x in seq)
next_for = lambda seq: 0 if zeros(seq) else seq[-1] + next_for(diffs(seq))

print(sum(next_for(seq) for seq in histories))
