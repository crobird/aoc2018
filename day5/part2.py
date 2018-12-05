#!/usr/bin/env python

# Wrong answer: 10497

import re
from string import ascii_lowercase

pattern = re.compile("({})".format('|'.join(["{0}{1}|{1}{0}".format(c, c.upper()) for c in ascii_lowercase])))

def one_pass(s):
	return re.sub(pattern, '', s)

with open("input.txt", "r") as fh:
	puzzle = fh.read()
	puzzle = puzzle.strip()

# puzzle = "dabAcCaCBAcCcaDA"

polymer = None
shortest = None
for c in ascii_lowercase:
	before = re.sub(c, '', puzzle, flags=re.IGNORECASE)
	count = 0
	go = True
	while go:
		after = one_pass(before)
		count += 1
		if after == before:
			go = False
		before = after

	l = len(before)
	if shortest is None or l < shortest:
		shortest = l
		polymer = c

print("Shortest length={} for polymer={}".format(shortest, polymer))