#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])
seeds = [int(s) for s in lines[0].split(":")[1].split()]
seed_ranges = {(seeds[i], seeds[i] + seeds[i + 1] - 1) for i in range(0, len(seeds), 2)}
breaks = [idx for idx, line in enumerate(lines) if line == ""]

mapping_stages = []
for idx in range(len(breaks)):
    m = []
    for i in range(breaks[idx] + 2, breaks[idx + 1] if idx + 1 < len(breaks) else len(lines)):
        [t, f, l] = [int(s) for s in lines[i].split()]
        r = [t, (f, f + l - 1)]
        m.append(r)

    mapping_stages.append(m)


def translate_range(input_range, source_range, to_start):
    start, end = (
        max(input_range[0], source_range[0]),
        min(input_range[1], source_range[1]),
    )

    moved = None
    unmoved = set()
    if start <= end:
        moved = (start - source_range[0] + to_start, end - source_range[0] + to_start)

        if input_range[0] < start:
            unmoved.add((input_range[0], start - 1))
        if end < input_range[1]:
            unmoved.add((end + 1, input_range[1]))
    else:
        unmoved.add(input_range)

    return moved, unmoved


def map_range(input_range, mapping):
    unmoved = set([input_range])
    moved = set()
    for to_start, source_range in mapping:
        next_unmoved = set()
        for range in unmoved:
            m, u = translate_range(range, source_range, to_start)
            if m:
                moved.add(m)
            next_unmoved |= u
        unmoved = next_unmoved

    return moved | unmoved


def map_ranges(ranges, mapping):
    return {r for mapped in [map_range(range, mapping) for range in ranges] for r in mapped}


def run(ranges):
    return reduce(lambda curr, mapping: map_ranges(curr, mapping), mapping_stages, ranges)


starts = {r[0] for r in run(seed_ranges)}
print(min(starts))
