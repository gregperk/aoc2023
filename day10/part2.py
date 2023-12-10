#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=['example9.txt', 'example12.txt', 'example14.txt', 'input.txt'])
lines = ["."*len(lines[0])] + lines + ["."*len(lines[0])]
lines = ['.' + line + '.' for line in lines]
start_loc = [(x,y) for y,line in enumerate(lines) for x,c in enumerate(line) if c == 'S'][0]

scratch = [['.'] * len(line) for line in lines]

def show(grid):
    print('\n'.join([''.join(line) for line in grid]))

def peek(loc):
    x,y = loc
    return lines[y][x]

def poke_scratch(loc, value):
    x,y = loc
    scratch[y][x] = value

def peek_scratch(loc):
    x,y=loc
    return scratch[y][x]

def step(loc, delta):
    x,y = loc
    dx,dy = delta
    return (x+dx, y+dy)

# entry_delta, symbol -> left_deltas, right_deltas, exit_delta
translator = {
    ((0,-1), '|'): ([(-1,0)], [(+1,0)], (0,-1)),
    ((0,+1), '|'): ([(+1,0)], [(-1,0)], (0,+1)),
    ((+1,0), '-'): ([(0,-1)], [(0,+1)], (+1,0)),
    ((-1,0), '-'): ([(0,+1)], [(0,-1)], (-1,0)),
    ((0,+1), 'L'): ([], [(-1,0),(0,+1)], (+1,0)),
    ((-1,0), 'L'): ([(0,+1),(-1,0)], [], (0,-1)),
    ((0,+1), 'J'): ([(+1,0),(0,+1)], [], (-1,0)),
    ((+1,0), 'J'): ([], [(0,+1),(+1,0)], (0,-1)),
    ((+1,0), '7'): ([(0,-1),(+1,0)], [], (0,+1)),
    ((0,-1), '7'): ([], [(+1,0),(0,-1)], (-1,0)),
    ((0,-1), 'F'): ([(-1,0),(0,-1)], [], (+1,0)),
    ((-1,0), 'F'): ([], [(0,-1),(-1,0)], (0,+1)),
}

def start_deltas(loc):
    return [delta for delta in [(-1, 0), (0, -1), (0, 1), (1, 0)] 
            if (delta, peek(step(loc, delta))) in translator.keys()]

def is_empty(loc):
    x,y = loc
    return peek_scratch(loc) == '.' if x>=0 and x<len(lines[0]) and y>=0 and y<len(lines) else False

def fill(loc, mark):
    if not is_empty(loc):
        return 0

    queue = deque([loc])
    visited = set([loc])
    count = 0

    while queue:
        curr = queue.popleft()
        poke_scratch(curr, mark)
        count += 1
        todos = [step(curr, delta) for delta in [(-1, 0), (0, -1), (0, 1), (1, 0)]]
        todos = [t for t in todos if is_empty(t) and t not in visited]
        queue.extend(todos)
        visited.update(todos)

    return count

def walk(loc, filling=False):
    delta = start_deltas(loc)[0]

    lcount = rcount = 0
    while True:
        if not filling:
            poke_scratch(loc, '*')
        loc = step(loc, delta)
        symbol = peek(loc)
        if symbol == 'S':
            break

        lefts, rights, delta = translator[(delta, symbol)]
        if filling:
            for l_delta in lefts:
                lcount += fill(step(loc,l_delta), 'L')
            for r_delta in rights:
                rcount += fill(step(loc,r_delta), 'R')
    
    return lcount, rcount

walk(start_loc)
lcount, rcount = walk(start_loc, filling=True)

print(rcount if peek_scratch((0,0)) == 'L' else lcount)
