#!/usr/bin/env python

import re
from copy import copy, deepcopy

class Sky(object):
	def __init__(self, min_x, min_y, max_x, max_y):
		self.min_x = min_x
		self.min_y = min_y
		self.max_x = max_x
		self.max_y = max_y

		self.x_offset = abs(self.min_x) if self.min_x < 0 else 0
		self.y_offset = abs(self.min_y) if self.min_y < 0 else 0

		self.sky = [[list() for x in range(self.max_x + self.x_offset + 1)] for y in range(self.max_y + self.y_offset + 1)]
		self.next_sky = [[list() for x in range(self.max_x + self.x_offset + 1)] for y in range(self.max_y + self.y_offset + 1)]

		print("Building sky...")
		print("{},{} -> {},{}".format(min_x, min_y, max_x, max_y))
		print("Array: {} x {}".format(len(self.sky), len(self.sky[0])))

	def __repr__(self):
		return self.get_skyprint(self.sky)

	def print_sky(self, sky_to_print):
		print(self.get_skyprint(sky_to_print))

	def get_skyprint(self, sky_to_print):
		lines = []
		for y in range(len(sky_to_print)):
			lines.append("".join(['#' if len(sky_to_print[y][x]) else '.' for x in range(len(sky_to_print[0]))]))
		return "\n".join(lines)

	def add(self, star):
		self.sky[star.y + self.y_offset][star.x + self.x_offset].append(star)

	def vertcount(self):
		# determine how many stars have vertical neighbors
		count = 0
		for y in range(len(self.sky)):
			for x in range(len(self.sky[0])):
				if len(self.sky[y][x]):
					if y > 0 and self.sky[y-1][x]:
						count += 1
						continue
					if (y+1) < len(self.sky) and self.sky[y+1][x]:
						count += 1
						continue
		return count

	def copy(self):
		return deepcopy(self.sky)

	def next(self):
		for y in range(len(self.sky)):
			for x in range(len(self.sky[0])):
				for i in range(len(self.sky[y][x])):
					s = self.sky[y][x][i]
					new_x = x + s.vx
					new_y = y + s.vy
					try:
						self.next_sky[new_y][new_x].append(s)
					except Exception:
						print("sky = [{}][{}], star = [{}][{}] -> [{}][{}]".format(
							len(self.sky), len(self.sky[0]), y, x, new_y, new_x))

		for y in range(len(self.sky)):
			for x in range(len(self.sky[0])):
				self.sky[y][x] = [s for s in self.next_sky[y][x]]
				self.next_sky[y][x] = []



class Star(object):
	def __init__(self, x, y, vx, vy):
		self.x  = x
		self.y  = y
		self.vx = vx
		self.vy = vy

	def __repr__(self):
		return "{},{} - {},{}".format(self.x, self.y, self.vx, self.vy)


def main(args):

	with open("input.txt", "r") as fh:
		file = fh.read()

	# file = """
	# position=< 9,  1> velocity=< 0,  2>
	# position=< 7,  0> velocity=<-1,  0>
	# position=< 3, -2> velocity=<-1,  1>
	# position=< 6, 10> velocity=<-2, -1>
	# position=< 2, -4> velocity=< 2,  2>
	# position=<-6, 10> velocity=< 2, -2>
	# position=< 1,  8> velocity=< 1, -1>
	# position=< 1,  7> velocity=< 1,  0>
	# position=<-3, 11> velocity=< 1, -2>
	# position=< 7,  6> velocity=<-1, -1>
	# position=<-2,  3> velocity=< 1,  0>
	# position=<-4,  3> velocity=< 2,  0>
	# position=<10, -3> velocity=<-1,  1>
	# position=< 5, 11> velocity=< 1, -2>
	# position=< 4,  7> velocity=< 0, -1>
	# position=< 8, -2> velocity=< 0,  1>
	# position=<15,  0> velocity=<-2,  0>
	# position=< 1,  6> velocity=< 1,  0>
	# position=< 8,  9> velocity=< 0, -1>
	# position=< 3,  3> velocity=<-1,  1>
	# position=< 0,  5> velocity=< 0, -1>
	# position=<-2,  2> velocity=< 2,  0>
	# position=< 5, -2> velocity=< 1,  2>
	# position=< 1,  4> velocity=< 2,  1>
	# position=<-2,  7> velocity=< 2, -2>
	# position=< 3,  6> velocity=<-1, -1>
	# position=< 5,  0> velocity=< 1,  0>
	# position=<-6,  0> velocity=< 2,  0>
	# position=< 5,  9> velocity=< 1, -2>
	# position=<14,  7> velocity=<-2,  0>
	# position=<-3,  6> velocity=< 2, -1>
	# """

	max_x = None
	max_y = None
	min_x = None
	min_y = None
	input = file.strip().split("\n")
	stars = []
	for line in input:
		mo = re.match(r'\s*position=<\s?(-?\d+),\s+(-?\d+)> velocity=<\s?(-?\d+),\s+(-?\d+)>', line)
		if not mo:
			print("Can't regex line")
			exit(1)
		(x,y,vx,vy) = map(int, (mo.group(1), mo.group(2), mo.group(3), mo.group(4)))
		s = Star(x=x, y=y, vx=vx, vy=vy)
		if max_x is None or x > max_x:
			max_x = x
		if min_x is None or x < min_x:
			min_x = x
		if max_y is None or y > max_y:
			max_y = y
		if min_y is None or y < min_y:
			min_y = y
		stars.append(s)

	sky = Sky(min_x, min_y, max_x, max_y)
	for s in stars:
		sky.add(s)

	stars = [] # Clear out stars for whatever that's worth

	print("{}\n".format(sky))
	moves         = 0
	max_vertcount = 0
	max_movenum   = 0
	sky_at_max    = None

	while True:
		moves += 1
		sky.next()
		vertcount = sky.vertcount()
		if vertcount > max_vertcount:
			previous_vertcount = max_vertcount
			max_vertcount = vertcount
			max_movenum = moves
			sky_at_max = sky.copy()
			if previous_vertcount > 0:
				pct_increase = ((max_vertcount - previous_vertcount) / previous_vertcount) * 100
				if pct_increase > 50 and max_vertcount > 30:
					break
		if args.n_times and moves == args.n_times:
			break

		print("{}\n".format(sky))


	print("Max vertcount = {}, move number: {}".format(max_vertcount, moves))
	print(sky.print_sky(sky_at_max))


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--n_times", type=int, help="number of times to go (default is auto)")
	args = parser.parse_args()

	main(args)