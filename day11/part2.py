#!/usr/bin/env python


import re
import math


# not 258,189,7
# not 239,260,10
# not 161,267,11

def compute_power_level(x, y, serial_number):
	x = x + 1
	y = y + 1
	rack_id = x + 10
	p = ((rack_id * y) + serial_number) * rack_id
	return (math.floor(p / 100) % 10) - 5

def get_box_score(grid, x, y, grid_size, last_grid_sum):
	if last_grid_sum is not None:
		return last_grid_sum + sum([grid[y+grid_size-1][x+a] + grid[y+a][x+grid_size-1] for a in range(grid_size)]) - grid[y+grid_size-1][x+grid_size-1]

	grid_sum = 0
	for i in range(grid_size):
		for j in range(grid_size):
			grid_sum += grid[y+i][x+j]
	return grid_sum

def main(args):

	serial_number = args.serial
	grid_size     = 300

	grid = [[compute_power_level(x,y,serial_number) for x in range(grid_size)] for y in range(grid_size)]

	if (args.x and args.y):
		print("Power for {},{} w/ serial {} is {}".format(args.x, args.y, serial_number, grid[args.y-1][args.x-1]))
		exit(0)

	max_bs = 0
	max_x = None
	max_y = None
	max_grid_size = None
	for y in range(grid_size):
		for x in range(grid_size):
			last_grid_sum = None
			for g in range(grid_size):
				this_grid_size = g + 1
				if (x <= grid_size - this_grid_size) and (y <= grid_size - this_grid_size):
					old_lgs = last_grid_sum
					last_grid_sum = get_box_score(grid, x, y, this_grid_size, last_grid_sum)
					if last_grid_sum > max_bs:
						max_bs = last_grid_sum
						max_x = x + 1
						max_y = y + 1
						max_grid_size = this_grid_size
				else:
					# Larger grid sizes won't work either
					break



	print("Max box score is {} at {},{},{}".format(max_bs, max_x, max_y, max_grid_size))



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-x", "--x", type=int, help="x")
	parser.add_argument("-y", "--y", type=int, help="y")
	parser.add_argument("-s", "--serial", type=int, help="serial number")
	args = parser.parse_args()

	main(args)