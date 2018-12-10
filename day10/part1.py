#!/usr/bin/env python


# Note: This code is super messy because I kept reworking how I was going to do it. I failed (foolishly)
# to see that I'd have problems generating lists as big as all of the galaxy of stars each time.

# I eventually realized that the universe of stars is shrinking, so I just needed to know when it stopped
# getting smaller. I reworked the code to calculate the size of the current star shape and then added
# input so I could print at a given time. That allowed it to be small enough to print then and also gave
# me the immediate answer to part 2.


import re


class Sky(object):
	def __init__(self, min_x, min_y, max_x, max_y):
		self.min_x = min_x
		self.min_y = min_y
		self.max_x = max_x
		self.max_y = max_y
		self.stars = []

		self.x_offset = abs(self.min_x) if self.min_x < 0 else 0
		self.y_offset = abs(self.min_y) if self.min_y < 0 else 0

	def __repr__(self):
		return self.get_skyprint(self.sky)

	def print_sky(self, sky_to_print):
		print(self.get_skyprint(sky_to_print))

	def get_skyprint(self, sky_to_print):
		lines = []
		for y in range(len(sky_to_print)):
			lines.append("".join(['#' if sky_to_print[y][x] else '.' for x in range(len(sky_to_print[0]))]))
		return "\n".join(lines)

	def add(self, star):
		self.stars.append(star)

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

	def size_at(self, n):
		new_stars = [s.at(n) for s in self.stars]
		min_x = min([s[0] for s in new_stars])
		max_x = max([s[0] for s in new_stars])
		min_y = min([s[1] for s in new_stars])
		max_y = max([s[1] for s in new_stars])
		return (max_x - min_x) * (max_y - min_y)

	def print_stars_at(self, n):
		new_stars = [s.at(n) for s in self.stars]
		min_x = min([s[0] for s in new_stars])
		max_x = max([s[0] for s in new_stars])
		min_y = min([s[1] for s in new_stars])
		max_y = max([s[1] for s in new_stars])
		print("min_x = {}, max_x = {}, min_y = {}, max_y = {}".format(min_x, max_x, min_y, max_y))
		sky = [[None for x in range(max_x + 1)] for y in range(max_y + 1)]
		for s in new_stars:
			sky[s[1]][s[0]] = '#'
		self.print_sky(sky)


class Star(object):
	def __init__(self, x, y, vx, vy):
		self.x  = x
		self.y  = y
		self.vx = vx
		self.vy = vy

	def __repr__(self):
		return "{},{} - {},{}".format(self.x, self.y, self.vx, self.vy)

	def at(self, n):
		return ((self.x + (self.vx * n)), (self.y + (self.vy * n)))


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

	if args.printmove:
		sky.print_stars_at(args.printmove)
		exit(0)

	stars = [] # Clear out stars for whatever that's worth

	moves         = 0
	max_vertcount = 0
	max_movenum   = 0
	sky_at_max    = None
	min_size = None

	while True:
		moves += 1
		size = sky.size_at(moves)
		if min_size is None or size < min_size:
			min_size = size
		else:
			print("it stopped shrinking on move {}, so smallest move was {}".format(moves, moves - 1))
			break



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--n_times", type=int, help="number of times to go (default is auto)")
	parser.add_argument("-p", "--printmove", type=int, help="move of number to print")
	args = parser.parse_args()

	main(args)