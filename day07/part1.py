#!/usr/bin/env python3
from aoc_util import *

lines = read_input_lines(default_idx=0, filenames=["example0.txt", "input.txt"])
hand_bids = [(parts[0], int(parts[1])) for line in lines if (parts := line.split())]

card_ranks = {card: rank for rank, card in enumerate(list("23456789TJQKA"))}

def hand_strength(hand_rank, hand):
    return reduce(lambda value, card: (value * 13) + card_ranks[card], hand, hand_rank)

def evaluate_hand(hand):
    counter = Counter(hand)
    counts = sorted(counter.values(), reverse=True)

    if counts[0] == 5:
        return hand_strength(7, hand)
    elif counts[0] == 4:
        return hand_strength(6, hand)
    elif counts[0] == 3 and counts[1] == 2:
        return hand_strength(5, hand)
    elif counts[0] == 3:
        return hand_strength(4, hand)
    elif counts[0] == counts[1] == 2:
        return hand_strength(3, hand)
    elif counts[0] == 2:
        return hand_strength(2, hand)
    else:
        return hand_strength(1, hand)

evaluated = list(map(lambda x: (x[1], evaluate_hand(x[0])), hand_bids))

ordered = sorted(evaluated, key=lambda x: x[1])

print(sum((i + 1) * x[0] for i, x in enumerate(ordered)))
