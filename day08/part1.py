#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=['example0.txt', 'example1.txt', 'input.txt'])
instructions = [0 if x == 'L' else 1 for x in list(lines[0])]
nodes = {g[0]:(g[1],g[2]) for l in lines if (g:=re_groups(r'(\w{3}) = \((\w{3}), (\w{3})\)', l))}

node = 'AAA'
for step, instr in enumerate(cycle(instructions)):
    node = nodes[node][instr]
    if node == 'ZZZ':
        print(step + 1)
        break
