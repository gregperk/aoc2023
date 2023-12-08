import sys
import re
from itertools import count, cycle, chain
from functools import reduce
from collections import Counter, deque, defaultdict, namedtuple
from math import gcd, lcm
from operator import concat, eq, gt, lt, ne, xor, mul, mod


def read_input_lines(default_idx=0, filenames=["input.txt"]):
    filename = filenames[default_idx if len(sys.argv) == 1 else int(sys.argv[1])]
    return [line.strip("\n") for line in open(filename)]


def re_groups(regex, str):
    matches = re.match(regex, str)
    return matches.groups() if matches else None


def range_and(a, b):
    return range(max(a.start, b.start), min(a.stop, b.stop))


def range_minus(a, b):
    i = range_and(a, b)
    if len(i) == 0:
        return [a]

    result = []
    if i.start > a.start:
        result.append(range(a.start, i.start))
    if i.stop < a.stop:
        result.append(range(i.stop, a.stop))

    return result
