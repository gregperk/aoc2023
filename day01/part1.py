#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=['example0.txt', 'input.txt'])

sum = 0
for line in lines:
    first = re.search(r"^\D*(\d)", line).group(1)
    line = line[::-1]
    last = re.search(r"^\D*(\d)", line).group(1)
    sum += int(first + last)

print(sum)
