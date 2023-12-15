#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 145), ('input.txt', 286104)])

boxes = defaultdict(lambda: [])

def hash(s):
    return reduce(lambda curr,next: ((curr+ord(next))*17)%256, s, 0)

def hashmap(s):
    if '=' in s:
        str,num = s.split('=')
        lst = boxes[hash(str)]
        indices = [i for i,v in enumerate(lst) if v[0] == str]
        if indices:
            lst[indices[0]] = (str,int(num))
        else:
            lst.append((str,int(num)))
    else:
        str = s[:-1]
        lst = boxes[hash(str)]
        indices = [i for i,v in enumerate(lst) if v[0] == str]
        if indices:
            del lst[indices[0]]

def solution(line):
    for s in line.split(','):
        hashmap(s)

    total = 0
    for box_number,lenses in boxes.items():
        if not lenses:
            continue
        for idx,(_label,f) in enumerate(lenses):
            total += (box_number+1) * (idx+1) * (f)
    
    return total

assert_solution(solution(next(case_lines())))
