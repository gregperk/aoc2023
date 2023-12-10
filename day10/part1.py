#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=['example1.txt', 'example2.txt', 'example3.txt', 'example4.txt', 'example5.txt', 'example7.txt', 'input.txt'])
start_loc = [(x,y) for y,line in enumerate(lines) for x,c in enumerate(line) if c == 'S'][0]
        
# entry_delta, symbol -> exit_delta
translator = {
    ((0,-1), '|'): (0,-1),
    ((0,+1), '|'): (0,+1),
    ((+1,0), '-'): (+1,0),
    ((-1,0), '-'): (-1,0),
    ((0,+1), 'L'): (+1,0),
    ((-1,0), 'L'): (0,-1),
    ((0,+1), 'J'): (-1,0),
    ((+1,0), 'J'): (0,-1),
    ((+1,0), '7'): (0,+1),
    ((0,-1), '7'): (-1,0),
    ((0,-1), 'F'): (+1,0),
    ((-1,0), 'F'): (0,+1),
}

def start_deltas(loc):
    return [delta for delta in [(-1, 0), (0, -1), (0, 1), (1, 0)] 
            if (delta, peek(step(loc, delta))) in translator.keys()]

def peek(loc):
    x,y = loc
    return lines[y][x]

def step(loc, delta):
    x,y = loc
    dx,dy = delta
    return (x+dx, y+dy)

def walk(loc):
    delta = start_deltas(loc)[0]

    steps = 0
    while True:
        steps += 1
        loc = step(loc, delta)
        symbol = peek(loc)
        if symbol == 'S':
            break
        delta = translator[(delta, symbol)]
    
    return steps

print(walk(start_loc) // 2)