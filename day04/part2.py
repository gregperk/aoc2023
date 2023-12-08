#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])

card_counts = [1] * len(lines)
for line_idx, line in enumerate(lines):
    winners, holding = line.split(":")[1].split("|")
    n_matching = len(set(winners.split()) & set(holding.split()))
    for offset in range(n_matching):
        card_counts[line_idx + 1 + offset] += card_counts[line_idx]

print(sum(card_counts))
