#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 5), ('input.txt', 475)])

# read and sort the brick definitions vertically
brick_defs = [[(int(g[0]),int(g[1]),int(g[2])),(int(g[3]),int(g[4]),int(g[5]))] for line in case_lines() if (g:=re_groups(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', line))]
brick_defs.sort(key=lambda s: (s[0][2],s[1][2]))

# instantiate them in a dict mapping to their indices
min_x = min_y = sys.maxsize
max_x = max_y = -sys.maxsize
bricks = []
for idx,[start,end] in enumerate(brick_defs):
    x1,y1,z1 = start
    x2,y2,z2 = end
    min_x,max_x = min(x1,x2,min_x),max(x1,x2,max_x)
    min_y,max_y = min(y1,y2,min_y),max(y1,y2,max_y)
    brick = {(x,y,z):idx for x in range(x1,x2+1) for y in range(y1,y2+1) for z in range(z1,z2+1)}
    bricks.append(brick)

# prep ground for collision-detection to find bricks' landing places
ground = {(x,y,0):-1 for x in range(min_x,max_x+1) for y in range(min_y,max_y+1)}

# from the lowest to the highest bricks, find their landing places one step shy of collision
# and retain the brick(s) they collided with
def rests_on():
    volume = dict(ground)
    result = []
    for brick in bricks:
        distance = 0
        for dist in count():
            collisions = {volume[(x,y,z-dist)] for x,y,z in brick if (x,y,z-dist) in volume}
            if collisions:
                break
            else:
                distance = dist

        result.append(collisions)
        volume.update({(x,y,z-distance):v for (x,y,z),v in brick.items()})

    return result

# a brick is not removable if another brick depends on only that one
def all_removable():
    on = rests_on()
    removable = set(range(len(on)))
    for idx in range(len(on)):
        if len(on[idx]) == 1:
            removable -= on[idx]
    
    return removable

assert_solution(len(all_removable()))

