#!/usr/bin/env python

import re


class Claim(object):
	def __init__(self, line):
		match_obj = re.match(r'\#(\d+)\s+\@\s+(\d+),(\d+):\s+(\d+)x(\d+)', line)
		if not match_obj:
			print("Error parsing line: {}".format(line))
			exit(1)
		(self.id, self.left, self.top, self.width, self.height) = map(int, match_obj.groups())

	def __repr__(self):
		return "#{} @ {},{}: {}x{}".format(self.id, self.left, self.top, self.width, self.height)

	@property
	def left_margin_plus_width(self):
		return self.left + self.width

	@property
	def top_margin_plus_height(self):
		return self.top + self.height


class Fabric(object):
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.fabric = [[None for x in range(width)] for y in range(height)]
		self.overlap = 0

	def __repr__(self):
		outlines = []
		for i in range(self.height):
			l = []
			for j in range(self.width):
				l.append('.' if self.fabric[i][j] is None else self.fabric[i][j])
			outlines.append("".join(l))
		return "\n".join(outlines)

	def apply_claim(self, claim):
		for i in range(claim.top, claim.top_margin_plus_height):
			for j in range(claim.left, claim.left_margin_plus_width):
				if self.fabric[i][j] is None:
					self.fabric[i][j] = 'T'
				elif self.fabric[i][j] == 'T':
					self.fabric[i][j] = 'X'
					self.overlap += 1





with open("input.txt", "r") as fh:
	file = fh.read()

# file = """
# #1 @ 1,3: 4x4
# #2 @ 3,1: 4x4
# #3 @ 5,5: 2x2
# """

lines = file.split("\n")
claims = []
max_width = 0
max_height = 0
for line in lines:
	if line == '':
		continue
	c = Claim(line)
	if c.left_margin_plus_width > max_width:
		max_width = c.left_margin_plus_width
	if c.top_margin_plus_height > max_height:
		max_height = c.top_margin_plus_height
	claims.append(c)

f = Fabric(max_width, max_height)
for c in claims:
	f.apply_claim(c)

# print(f)
print(f.overlap)
