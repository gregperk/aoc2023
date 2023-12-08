#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=['example0.txt', 'example1.txt', 'input.txt'])

digits = {str(n): str(n) for n in range(10)}
digits = digits | {
    s: str(n)
    for n, s in enumerate(["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"])
}

def first_digit(str, reversed=False):
    if reversed:
        str = str[::-1]
    first_idx = sys.maxsize
    first_digit = None
    for k, v in digits.items():
        if reversed:
            k = k[::-1]
        idx = str.find(k)
        if idx >= 0 and idx < first_idx:
            first_idx = idx
            first_digit = v
    return first_digit

sum = 0
for line in lines:
    sum += int(first_digit(line) + first_digit(line, reversed=True))

print(sum)
