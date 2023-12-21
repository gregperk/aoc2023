#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=-1, cases=[('example0.txt', 62), ('example1.txt', 97), ('example2.txt', 130), ('example3.txt', 124), ('example4.txt', 52), ('input.txt', 49897)])

dig_plan = [(g[0],int(g[1]),int(g[2],base=16)) for line in case_lines() if (g:=re_groups(r'([UDLR]) (\d+) \(#(......)\)', line))]

canvas = defaultdict(lambda: 0)

delta = {
    'U': (0,-1),
    'R': (+1,0),
    'D': (0,+1),
    'L': (-1,0),
}

min_x = 0
max_x = 0
min_y = 0
max_y = 0

def step(pos, dir):
    x,y = pos
    dx,dy = dir
    return (x+dx, y+dy)

def draw(pos, dir, color):
    global min_x, max_x, min_y, max_y
    x,y = pos
    dx,dy = dir

    nx,ny = x+dx, y+dy

    min_x = min(min_x, nx)
    max_x = max(max_x, nx)

    min_y = min(min_y, ny)
    max_y = max(max_y, ny)

    canvas[(x,y)] = color
    canvas[(nx,ny)] = color

    return nx,ny

def fill(loc, fill_color):
    queue = deque([loc])
    visited = set([loc])
    count = 0

    while queue:
        curr = queue.popleft()
        canvas[curr] = fill_color
        count += 1
        todos = [step(curr, delta) for delta in [(-1, 0), (0, -1), (0, 1), (1, 0)]]
        todos = [(x,y) for x,y in todos if x>=min_x and x<=max_x and y>=min_y and y<=max_y]
        todos = [loc for loc in todos if canvas[loc]==0 and loc not in visited]
        queue.extend(todos)
        visited.update(todos)

    return count

def paint():
    curr = (0,0)
    for dir,dist,color in dig_plan:
        for _n in range(dist):
            curr = draw(curr, delta[dir], color)

def show():
    inside = 0
    border = 0
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            color = canvas[(x,y)]
            if color == 1:
                char = '.'
            elif color == 0:
                char = ' '
                inside += 1
            else:
                char = '#'
                border += 1
            print(char, end='')
        print(' ')
    print(f'width={max_x-min_x+1}, hight={max_y-min_y+1}')
    print(f'inside={inside}, border={border}, total={inside+border}')
    return inside,border

paint()
min_x -= 1
min_y -= 1
max_x += 1
max_y += 1
fillcount = fill((min_x,min_y), 1)
print(f'(outside) filled={fillcount}')
inside,border = show()

assert_solution(inside+border)
