#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 0), ('input.txt', 16172)])

particles = [(tuple(vals[0:2]),tuple(vals[3:5])) for line in case_lines() if (vals:=[int(s) for s in re.split(r'[@,]', line)])]

def intersect(p1, p2):
    (x1, y1),(dx1,dy1) = p1
    (x2, y2),(dx2,dy2) = p2

    if dx1 * dy2 == dy1 * dx2:
        return (None,None),(None,None) # no intersection, parallel paths

    t1 = ((x2 - x1) * dy2 - (y2 - y1) * dx2) / (dx1 * dy2 - dy1 * dx2)
    t2 = ((x1 - x2) * dy1 - (y1 - y2) * dx1) / (dx2 * dy1 - dy2 * dx1)

    intersection = (x1 + t1 * dx1, y1 + t1 * dy1)

    return intersection, (t1, t2)

count = 0
for p1,p2 in combinations(particles,2):
    (x,y),(t1,t2) = intersect(p1, p2)
    if x != None and t1 > 0 and t2 > 0 and x >= 200000000000000 and x <= 400000000000000 and y >= 200000000000000 and y <= 400000000000000:
        count += 1

assert_solution(count)
