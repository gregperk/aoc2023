#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 1320), ('input.txt', 517015)])

def hash(s):
    return reduce(lambda curr,next: ((curr+ord(next))*17)%256, s, 0)

def solution(line):
    return sum(hash(s) for s in line.split(','))

assert_solution(solution(next(case_lines())))
