#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])
width = len(lines[0])
height = len(lines)
part_nums = [{(m.start(), m.end()-1, int(m.group())) for m in re.finditer(r'\d+', line)} for line in lines]

def find_hits(x,y):
    probes = [(dx+x,dy+y) for dx in [-1,0,+1] for dy in [-1,0,+1] if dx+x >= 0 and dx+x < width and dy+y >= 0 and dy+y < height]
    hits = {(py,start,end,value) for px,py in probes for (start,end,value) in part_nums[py] if start <= px and px <= end}

    for line, start, end, value in hits:
        part_nums[line].remove((start,end,value))

    return [hit[-1] for hit in hits]

answer = 0

for y,line in enumerate(lines):
    for x,c in enumerate(line):
        if c not in '.0123456789':
            hits = find_hits(x,y)
            answer += sum(hits)

print(answer)
