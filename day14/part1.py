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
	recipes = recipes + str(total)
	return recipes

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
	for i in range(args.num + args.extra):
		recipes = get_new_recipes(recipes, elf1, elf2)
		# print("--")
		# print("{}".format(recipe_str(recipes, elf1, elf2)))
		old_elf1 = elf1
		old_elf2 = elf2
		move1 = 1 + int(recipes[elf1])
		move2 = 1 + int(recipes[elf2])
		elf1 = (elf1 + move1) % len(recipes)
		elf2 = (elf2 + move2) % len(recipes)
		# print("recipe length: {}".format(len(recipes)))
		# print("elf1 @ [{}] moves {}, to index {}".format(old_elf1, move1, elf1))
		# print("elf2 @ [{}] moves {}, to index {}".format(old_elf2, move2, elf2))
		# print("{}".format(recipe_str(recipes, elf1, elf2)))
		if len(recipes) > args.num + args.extra:
			break
	print("{} recipes after {} recipes = {}".format(args.extra, args.num, recipes[args.num:args.num+args.extra]))



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--num", type=int, help="Number of recipes")
	parser.add_argument("-x", "--extra", type=int, help="Number of recipes after to return (default 10)", default=10)
	args = parser.parse_args()

	main(args)