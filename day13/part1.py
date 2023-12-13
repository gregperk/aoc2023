#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[("example0.txt", 405), ("input.txt", 30802)])

patterns = []
pattern = []
for line in case_lines():
    if line:
        pattern.append(line)
    else:
        patterns.append(pattern)
        pattern = []
patterns.append(pattern)


def horizontal_reflection(pattern):
    for i in range(0, len(pattern) - 1):
        if pattern[i] == pattern[i + 1]:
            foo = min(i, len(pattern) - (i + 1) - 1) + 1
            for j in range(1, foo):
                if pattern[i - j] != pattern[i + 1 + j]:
                    break
            else:
                return i + 1
    return None

def col(pattern, n):
    return [row[n] for row in pattern]

def vertical_reflection(pattern):
    for i in range(0, len(pattern[0]) - 1):
        if col(pattern, i) == col(pattern, i + 1):
            foo = min(i, len(pattern[0]) - (i + 1) - 1) + 1
            for j in range(1, foo):
                if col(pattern, i - j) != col(pattern, i + 1 + j):
                    break
            else:
                return i + 1
    return None

total = 0
for p in patterns:
    rows = horizontal_reflection(p)
    cols = vertical_reflection(p)
    val = 100 * rows if rows else cols
    total += val

assert_solution(total)
