#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example1.txt', 21), ('input.txt', 8022)])

rows = [(parts[0], list(map(int, parts[1].split(',')))) for line in case_lines() if (parts:=line.split())]

# take #-pattern (no ?'s) and see if the runs fit it!
def fits(pattern, runs):
    pass
    parts = list(filter(lambda x: x != 0, map(len, re.split(r'\.+', pattern))))
    return parts == runs

# build all uncorrupted posibile patterns from a corrupted pattern
def decorrupted_fits(corrupted, runs):
    atomized = list(corrupted)
    positions = [i for i,c in enumerate(atomized) if c == '?']
    variants = [f'{v:0{len(positions)}b}' for v in range(pow(2, len(positions)))]
    count = 0
    for variant in variants:
        foo = atomized[:]
        for (p,v) in zip(positions, variant):
            foo[p] = '.' if v == '0' else '#'
        if fits(''.join(foo), runs):
            count += 1
    return count

total = 0
for c,r in rows:
    total += decorrupted_fits(c,r)

assert_solution(total)
