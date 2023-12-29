#!/usr/bin/env python3
from aoc_util import *
BIG = sys.maxsize
set_cases(default_idx=0, cases=[('example0.txt', 62), ('example1.txt', 97), ('example2.txt', 130), ('example3.txt', 122), ('example4.txt', 52), ('example5.txt', 52), ('example6.txt', 52), ('example7.txt', 64), ('input.txt', 49897)])

if True:
    # Part-1 original encoding (what all of the above case solutions are set to test)
    dig_plan = [(g[0],int(g[1])) for line in case_lines() if (g:=re_groups(r'([UDLR]) (\d+) \(#(......)\)', line))]
    nodraw = False # debug mode to watch it work on small cases
else:
    # Part-2 hard-mode encoding
    dig_plan = [(int(g[1]),int(g[0],base=16)) for line in case_lines() if (g:=re_groups(r'.*\(#(.....)(.)\)', line))]
    nodraw = True

dir_delta = {
      0: (+1,0),
    'R': (+1,0),
      1: (0,+1),
    'D': (0,+1),
      2: (-1,0),
    'L': (-1,0),
      3: (0,-1),
    'U': (0,-1),
}

def plan_edges(dig_plan):
    edges = []
    curr = (0,0)
    for direction,length in dig_plan:
        x1,y1 = curr
        dx,dy = dir_delta[direction]
        x2 = x1 + dx*length
        y2 = y1 + dy*length
        next = (x2,y2)
        edges.append((min(curr,next),max(curr,next)))
        curr = next

    def sort_key(edge):
        ((ax,ay),(bx,by)) = edge
        return (ay,by,ax,bx)

    edges.sort(key=sort_key)
    return edges

def bounding_box(edges):
    tlx,tly = +BIG,+BIG
    brx,bry = -BIG,-BIG
    for ((x1,y1),(x2,y2)) in edges:
        tlx = min(tlx,x1)
        tly = min(tly,y1)
        brx = max(brx,x2)
        bry = max(bry,y2)

    return ((tlx,tly), (brx,bry))

def translated_edges(edges, dx, dy):
    return [((ax+dx, ay+dy), (bx+dx, by+dy)) for (ax, ay), (bx, by) in edges]

def draw_edges(edges):
    (tlx,tly),(brx,bry) = bounding_box(edges)
    dx,dy = -tlx,-tly
    tlx,tly,brx,bry = 0, 0, brx+dx, bry+dy

    if nodraw:
        return [[]], dx, dy

    grid = [['.']*(brx+1) for _y in range(bry+1)]
    for (x1,y1),(x2,y2) in edges:
        pass
        for x in range(x1+dx,x2+dx+1):
            for y in range(y1+dy,y2+dy+1):
                grid[y][x] = '#'

    return grid, dx, dy

def grid_str(grid):
    return '\n'.join([''.join(row) for row in grid])


def fill(grid, char, x1, y1, x2, y2):
    if nodraw:
        return max(0,(x2-x1+1))*max(0,(y2-y1+1))

    count = 0
    warnings = []
    for x in range(x1,x2+1):
        for y in range(y1, y2+1):
            if '*' == grid[y][x]:
                warnings.append((x,y))
            grid[y][x] = char
            count += 1

    if warnings:
        print(f'{char} ran over * in fill of ({x1},{y1})..({x2},{y2}) at locations {", ".join(str(w) for w in warnings)}')

    return count

def area():
    edges = plan_edges(dig_plan)
    grid,dx,dy = draw_edges(edges)
    edges = [(x1,x2,y1) for ((x1,y1),(x2,y2)) in translated_edges(edges, dx, dy) if y1 == y2]

    total = 0
    active = set()

    def activate(x1,x2,y):
        for a1,a2,ay in active:
            if y == ay and max(x1,a1) <= min(x2,a2):
                # merge any overlapping
                active.remove((a1,a2,y))
                activate(min(x1,a1),max(x2,a2),y)
                break
        else:
            active.add((x1,x2,y))

        fill(grid,'=',x1,y,x2,y)

    def close(x1,x2,y):
        return fill(grid,'*',x1,y,x2,y)

    # close out all overlapping actives down to y-1, and
    # return the range of (possibly merged) relevant actives, 
    # ready for treatment at y
    def prep_overlapping_actives(x1,x2,y):
        nonlocal active, total

        results = []

        relevant = {a for a in active if max(x1, a[0])<=min(x2, a[1])}
        active -= relevant
        while relevant:
            relevant = sorted(relevant, key=lambda a: (a[2],a[0],a[1])) # first by y, then by x1, then by x2
            ax1,ax2,ay = relevant[0]
            if len(relevant) == 1:
                # there's only one, so close it out down to y-1
                total += fill(grid, '*', ax1, ay, ax2, y-1)
                results.append(relevant.pop(0)[0:2])
                # fill(grid, '=', results[-1][0], y, results[-1][1], y)
            elif ay < relevant[1][2]:
                # there are two, but at different elevations, so fill first down to level of second
                bx1,bx2,by = relevant[1]
                total += fill(grid, '*', ax1, ay, ax2, by-1)
                relevant[0] = (ax1,ax2,by)
            elif ax2 < relevant[1][0]:
                # there are two at the same elevation that don't overlap, so close the first down to y-1
                total += fill(grid, '*', ax1, ay, ax2, y-1)
                results.append(relevant.pop(0)[0:2])
                # fill(grid, '=', results[-1][0], y, results[-1][1], y)
            else: 
                # there are two at the same elevation that DO overlap, so merge them
                bx1,bx2,by = relevant[1]
                relevant[0:2] = [(min(ax1,bx1),max(ax2,bx2),ay)]

        return results

    print(grid_str(grid))

    for edge in edges:
        e1,e2,y = edge

        o = prep_overlapping_actives(e1,e2,y)
        if not o:
            activate(e1,e2,y)
            continue

        # strip off leading add/keep
        o1,o2 = o[0]
        a1,a2 = min(o1,e1),max(o1,e1)
        e1,e2 = (a2,e2)
        o[0] = (a2,o2)
        lead = a1!=a2
        if lead:
            activate(a1,a2,y)

        # strip off trailing add/keep
        o1,o2 = o[-1]
        a1,a2 = min(o2,e2),max(o2,e2)
        e1,e2 = (e1,a1)
        o[-1] = (o1,a1)
        trail = a1!=a2
        if trail:
            activate(a1,a2,y)

        gaps = [o[i+1][0] - o[i][1] - 1 for i in range(len(o)-1)]
        squeeze = [(a>0, b>0) for a,b in zip([1 if lead else 0]+gaps,gaps+[1 if trail else 0])]

        # emit internal overlaps (closes) and gaps (activates)
        for (o1,o2),gap,(squeeze_left,squeeze_right) in zip(o,gaps+[0],squeeze):
            total += close(o1+1 if squeeze_left else o1, o2-1 if squeeze_right else o2, y)
            if gap > 0:
                activate(o2,o2+gap+1,y)

    print(grid_str(grid))
    return total

total = area()
assert_solution(total)
