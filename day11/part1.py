#!/usr/bin/env python


import re
import math

def compute_power_level(x, y, serial_number):
	x = x + 1
	y = y + 1
	rack_id = x + 10
	p = ((rack_id * y) + serial_number) * rack_id
	return (math.floor(p / 100) % 10) - 5

def get_box_score(grid, x, y, box_x, box_y):
	sum = 0
	for i in range(box_y):
		for j in range(box_x):
			sum += grid[y+i][x+j]
	return sum

def main(args):

	serial_number = args.serial
	grid_size_x   = 300
	grid_size_y   = 300
	box_x         = 3
	box_y         = 3

	grid = [[compute_power_level(x,y,serial_number) for x in range(grid_size_x)] for y in range(grid_size_y)]

	if (args.x and args.y):
		print("Power for {},{} w/ serial {} is {}".format(args.x, args.y, serial_number, grid[args.y-1][args.x-1]))
		exit(0)

	max_bs = 0
	max_x = None
	max_y = None
	for y in range(grid_size_y):
		for x in range(grid_size_x):
			if (x <= grid_size_x - box_x) and (y <= grid_size_y - box_y):
				bs = get_box_score(grid, x, y, box_x, box_y)
				if bs > max_bs:
					max_bs = bs
					max_x = x + 1
					max_y = y + 1

	print("Max box score is {} at {}, {}".format(max_bs, max_x, max_y))



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-x", "--x", type=int, help="x")
	parser.add_argument("-y", "--y", type=int, help="y")
	parser.add_argument("-s", "--serial", type=int, help="serial number")
	args = parser.parse_args()

	main(args)