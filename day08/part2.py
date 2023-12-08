#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=['example2.txt', 'input.txt'])
instructions = [0 if x == 'L' else 1 for x in list(lines[0])]
nodes = {g[0]:(g[1],g[2]) for l in lines if (g:=re_groups(r'(\w{3}) = \((\w{3}), (\w{3})\)', l))}

class Ghost:
    def __init__(self, initial_node_name):
        self.curr = initial_node_name     
        self.seen = set()
        self.stops = []
        self.cycled = False                             

ghosts = [Ghost(name) for name in nodes.keys() if name[-1] == 'A']

def step_ghosts(step_number):
    for ghost in [g for g in ghosts if not g.cycled]:
        i_num = step_number % len(instructions)
        next = (i_num, nodes[ghost.curr][instructions[i_num]])
        if next in ghost.seen:
            ghost.cycled = True
        else:
            ghost.seen.add(next)
            ghost.curr = next[1]
            if next[1][-1] == 'Z':
                ghost.stops.append(step_number + 1)

for step_number in count(0):
    step_ghosts(step_number)
    if all(g.cycled for g in ghosts):
        break

print(lcm(*[x for g in ghosts for x in g.stops]))
