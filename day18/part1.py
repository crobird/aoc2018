#!/usr/bin/env python

import re
import enum

DIRECTIONS = [
	(0,-1),
	(0,1),
	(1,0),
	(-1,0),
	(-1,-1),
	(1,-1),
	(-1,1),
	(1,1)
]

def get_dir(x,y,dir):
	return (x+dir[0], y+dir[1])

class LandType(enum.Enum):
	OPEN       = 1
	TREES      = 2
	LUMBERYARD = 3

TileMap = {
	'.': LandType.OPEN, 
	'|': LandType.TREES, 
	'#': LandType.LUMBERYARD
}

TileMapReverse = {
	LandType.OPEN: '.',
	LandType.TREES: '|',
	LandType.LUMBERYARD: '#'
}

class Tile(object):
	def __init__(self, c = None):
		self.c = None
		self.type = None
		self.neighbors = {
			LandType.OPEN: 0,
			LandType.TREES: 0,
			LandType.LUMBERYARD: 0
		}
		if c:
			self.add_type_char(c)

	def __repr__(self):
		return self.c if self.c else ' '

	def add_type_char(self, c):
		self.c = c
		self.type = TileMap[c]

	def add_type(self, t):
		self.type = t
		self.c = TileMapReverse[t]



	def next_type(self):
		if self.type == LandType.OPEN and self.neighbors[LandType.TREES] >= 3:
			return LandType.TREES
		if self.type == LandType.TREES and self.neighbors[LandType.LUMBERYARD] >= 3:
			return LandType.LUMBERYARD
		if self.type == LandType.LUMBERYARD:
			if self.neighbors[LandType.TREES] >= 1 and self.neighbors[LandType.LUMBERYARD] >= 1:
				return LandType.LUMBERYARD
			else:
				return LandType.OPEN
		return self.type


class Board(object):
	# move here means intersection, not vehicle movement
	def __init__(self, input_file):
		self.input_file = input_file
		self.board = None
		self.parse_input_file(input_file)

	def __repr__(self):
		out = ["--------------------------------"]
		for y in range(len(self.board)):
			out.append("".join(map(str, self.board[y])))
		return "\n".join(out)

	@property
	def tree_count(self):
		total = 0
		for y in range(len(self.board)):
			total += sum(1 for x in self.board[y] if x.type == LandType.TREES)
		return total
	
	@property
	def lumberyard_count(self):
		total = 0
		for y in range(len(self.board)):
			total += sum(1 for x in self.board[y] if x.type == LandType.LUMBERYARD)
		return total
	
	def parse_input_file(self, filepath):
		with open(filepath, "r") as fh:
			input = fh.read()
		lines = input.split("\n")
		self.board = [[Tile() for x in range(len(lines[0].strip()))] for y in range(len(lines))]
		for y,line in enumerate(lines):
			for x,c in enumerate(line.strip()):
				t = self.board[y][x]
				t.add_type_char(c)
				for n in self.neighbors(x, y):
					self.board[n[1]][n[0]].neighbors[t.type] += 1


	def neighbors(self, x, y):
		n = []
		for d in DIRECTIONS:
			(dx,dy) = get_dir(x, y, d)
			if dy >= 0 and dy < len(self.board) and dx >= 0 and dx < len(self.board[0]):
				n.append((dx,dy))
		return n

	def next_minute(self):
		upcoming = [[Tile() for x in range(len(self.board[0]))] for y in range(len(self.board))]
		for y in range(len(self.board)):
			for x in range(len(self.board)):
				next_type = self.board[y][x].next_type()
				upcoming[y][x].add_type(next_type)
				for n in self.neighbors(x, y):
					upcoming[n[1]][n[0]].neighbors[next_type] += 1
		self.board = upcoming


def main(args):

	board = Board(args.file)
	minutes = args.minutes

	# print(board)
	for m in range(minutes):
		board.next_minute()
		print(board)


	answer = board.tree_count * board.lumberyard_count
	print("answer after {} minutes is {}".format(minutes, answer))




if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-m", "--minutes", type=int, help="minutes")
	parser.add_argument("-f", "--file", help="file")
	args = parser.parse_args()

	main(args)