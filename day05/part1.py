#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])
seeds = [int(s) for s in lines[0].split(":")[1].split()]
breaks = [idx for idx, line in enumerate(lines) if line == ""]

mapping_stages = []
for idx in range(len(breaks)):
    m = []
    for i in range(breaks[idx] + 2, breaks[idx + 1] if idx + 1 < len(breaks) else len(lines)):
        r = [int(s) for s in lines[i].split()]
        m.append(r)

    mapping_stages.append(m)


def run(seed):
    v = seed
    for m in mapping_stages:
        for [t, f, n] in m:
            if f <= v and v < f + n:
                v = t + v - f
                break
    return v


foo = [run(s) for s in seeds]
print(min(foo))
