#!/usr/bin/env python

import re
import enum

class RoadType(enum.Enum):
	CORNER_LEFT_UP    = 7


class Elf(object):
	# move here means intersection, not vehicle movement
	def __init__(self, c):
		self.car_type = getCarType(c)
		self.last_move = None

	def __repr__(self):
		return CAR_TYPES[self.car_type]

def get_new_recipes(recipes, elf1, elf2):
	r1 = recipes[elf1]
	r2 = recipes[elf2]
	total = int(r1) + int(r2)
	return str(total)

def recipe_str(recipes, elf1, elf2):
	output = ''
	for i,c in enumerate(recipes):
		o = ''
		if elf1 == i and elf2 == i:
			o = "[({})]".format(c)
		elif elf1 == i:
			o = "({})".format(c)
		elif elf2 == i:
			o = "[{}]".format(c)
		else:
			o = c
		output = "{}{}{}".format(output, ' ' if output else '', o) 
	return output

def main(args):
	recipes = '37'
	elf1 = 0
	elf2 = 1
	i = 0
	latest_length = len(args.num) + 2
	test_length = latest_length * -1
	latest = ''
	while True:
		new_recipes = get_new_recipes(recipes, elf1, elf2)
		recipes = recipes + new_recipes
		latest = latest + new_recipes
		if len(latest) > latest_length:
			latest = latest[latest_length:]
		old_elf1 = elf1
		old_elf2 = elf2
		move1 = 1 + int(recipes[elf1])
		move2 = 1 + int(recipes[elf2])
		elf1 = (elf1 + move1) % len(recipes)
		elf2 = (elf2 + move2) % len(recipes)
		i += 1

		if latest.find(args.num) != -1:
			idx = recipes.find(args.num)
			print("It took {} recipes to get to {}".format(idx, args.num))
			break



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--num", help="Number of recipes")
	args = parser.parse_args()

	main(args)