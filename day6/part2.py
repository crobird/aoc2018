#!/usr/bin/env python

import re

class Coord(object):
	def __init__(self, x, y, index):
		self.x = x
		self.y = y
		self.id = index

def print_board(board):
	for y in range(len(board)):
		line = []
		for x in range(len(board[0])):
			line.append('.' if board[y][x] is None else str(board[y][x]))
		print(''.join(line))


def mdist(x1, y1, x2, y2):
	return abs(x2 - x1) + abs(y2 - y1)

with open("input.txt", "r") as fh:
	file = fh.read()

# file = """
# 1, 1
# 1, 6
# 8, 3
# 3, 4
# 5, 5
# 8, 9
# """

lines = file.split("\n")
max_x = 0
max_y = 0
coords = {}
linenum = 0
for line in lines:
	linenum += 1
	if line == '':
		continue

	mo = re.match(r'(\d+),\s+(\d+)', line)
	if not mo:
		print("Bad news, regex didn't match for line: {}".format(line))
	x = int(mo.group(1))
	y = int(mo.group(2))
	coords[linenum] = Coord(x,y,linenum)
	if x > max_x:
		max_x = x
	if y > max_y:
		max_y = y

board = [[None for i in range(max_x+1)] for j in range(max_y+1)]

for i in range(len(board)):
	for j in range(len(board[0])):
		dist_total = 0
		for cid in coords:
			dist_total += mdist(j, i, coords[cid].x, coords[cid].y)

		if dist_total < 10000:
			board[i][j] = 'X'

total = 0
for y in range(len(board)):
	total += len([x for x in board[y] if x == 'X'])

print("total = {}".format(total))
