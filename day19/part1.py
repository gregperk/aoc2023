#!/usr/bin/env python3
from aoc_util import *
set_cases(default_idx=0, cases=[('example0.txt', 19114), ('input.txt', 353553)])

def ingest():
    workflows = {}
    ratings = []

    read_rules = True
    for line in case_lines():
        if not line:
            read_rules = False
            continue
        if read_rules:
            [name,rulestext] = re_groups(r'^(\w+){(.*)}', line)
            rules = []
            for ruletext in rulestext.split(','):
                g = re_groups(r'(([xmas])([<>])(\d+):)?(\w+)', ruletext)
                rule = dotdict(var=g[1],op=g[2],val=g[3],dest=g[4])
                if rule.val:
                    rule.val = int(rule.val)
                rules.append(rule)
            workflows[name] = rules
        else:
            [x,m,a,s] = re_groups(r'^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}', line)
            ratings.append(dict(x=int(x),m=int(m),a=int(a),s=int(s)))

    return workflows,ratings

def apply(rating, name, workflows):
    while True:
        rules = workflows[name]
        for r in rules:
            name = r.dest
            if r.var:
                if r.op == '<':
                    if rating[r.var] < r.val:
                        break
                else:
                    if rating[r.var] > r.val:
                        break
        if name in ['A','R']:
            return name

workflows, ratings = ingest()
total = 0
for rating in ratings:
    if apply(rating, "in", workflows) == 'A':
        total += sum(rating.values())

assert_solution(total)