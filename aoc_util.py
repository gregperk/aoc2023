import sys
import re
from itertools import count, cycle, chain, combinations
from functools import reduce
from collections import Counter, deque, defaultdict, namedtuple
from math import gcd, lcm
from operator import concat, eq, gt, lt, ne, xor, mul, mod
from typing import List, Tuple, Generator


def read_input_lines(default_idx: int = 0, filenames: List[str] = ["input.txt"]):
    filename = filenames[default_idx if len(sys.argv) == 1 else int(sys.argv[1])]
    return [line.strip("\n") for line in open(filename)]


_default_idx = None
_cases = None


def set_cases(
    default_idx: int = 0, cases: List[Tuple[str, int]] = [("input.txt", None)]
) -> None:
    global _default_idx, _cases
    _default_idx = default_idx
    _cases = cases


def case_lines() -> Generator[str, None, None]:
    global _default_idx, _cases
    filename, _ = _cases[_default_idx if len(sys.argv) == 1 else int(sys.argv[1])]
    return (line.strip("\n") for line in open(filename))


def assert_solution(answer: int) -> None:
    global _default_idx, _cases
    filename, expected = _cases[_default_idx if len(sys.argv) == 1 else int(sys.argv[1])]
    if answer == expected:
        print(f"{answer} ({filename})")
    else:
        print(f"{answer} != {expected} ({filename})")


def re_groups(regex: str, text: str) -> List[str]:
    matches = re.match(regex, text)
    return matches.groups() if matches else None


class dotdict(dict):
    """ Dictionary with dot-accessible keys. """
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
