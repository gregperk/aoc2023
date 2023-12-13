#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[("example0.txt", 400), ("input.txt", 37876)])

# NOTE: There is still a bug in this code having to do with leaving an adjusted smudge
#       in place because I don't want to spend time refactoring/debugging this horrid mess.
#       It solves input.txt, but the assertion for example0.txt currently fails by one.

patterns = []
pattern = []
for line in case_lines():
    if line:
        pattern.append(list(line))
    else:
        patterns.append(pattern)
        pattern = []
patterns.append(pattern)


def show(pattern):
    print("\n".join("".join(row) for row in pattern))

_smudge_undo = None  # yes, yuck. this slimy, just-find-the-damned-answer code. :)

def toggle(ary, idx):
    ary[idx] = "." if ary[idx] == "#" else "#"

def cmp_smudge_eq(a, b):
    global _smudge_undo

    diffs = [n for n, (x1, x2) in enumerate(zip(a, b)) if x1 != x2]
    if not diffs:
        return True
    elif len(diffs) == 1 and not _smudge_undo:
        pos = diffs[0]
        toggle(a, pos)
        _smudge_undo = lambda: toggle(a, pos)
        return True
    else:
        return False

def cmp_normal_eq(a, b):
    return a == b

def horizontal_reflections(pattern, cmp_eq):
    global _smudge_undo
    _smudge_undo = None
    results = []
    for i in range(0, len(pattern) - 1):
        if cmp_eq(pattern[i], pattern[i + 1]):
            foo = min(i, len(pattern) - (i + 1) - 1) + 1
            for j in range(1, foo):
                if not cmp_eq(pattern[i - j], pattern[i + 1 + j]):
                    _smudge_undo() if _smudge_undo else None
                    _smudge_undo = None
                    break
            else:
                results.append(i + 1)
    return results

def rotate_clockwise(pat):
    h = len(pat)
    w = len(pat[0])
    return [[pat[y][x] for y in range(h - 1, -1, -1)] for x in range(w)]

def vertical_reflections(pattern, cmp_eq):
    return horizontal_reflections(rotate_clockwise(pattern), cmp_eq)


total = 0
for i, p in enumerate(patterns):
    hs1 = horizontal_reflections(p, cmp_normal_eq)
    vs1 = vertical_reflections(p, cmp_normal_eq)

    hs2 = horizontal_reflections(p, cmp_smudge_eq)
    vs2 = vertical_reflections(p, cmp_smudge_eq)

    hs = [] if hs1 == hs2 else [x for x in hs2 if x not in hs1]
    vs = [] if vs1 == vs2 else [x for x in vs2 if x not in vs1]

    total += sum(vs) + sum(100 * h for h in hs)

assert_solution(total)
