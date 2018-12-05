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

go = True
before = puzzle
count = 0
while go:
	after = one_pass(before)
	count += 1
	if after == before:
		go = False
		print("Final string after {} passes, length: {})".format(count, len(after)))
	before = after
