#!/usr/bin/env python


import re

class Rule(object):
	def __init__(self, rule, outcome):
		self.rule = rule
		self.outcome = is_plant(outcome)
		self.bools = [is_plant(x) for x in self.rule]

	def __repr__(self):
		return "".join(['#' if x else '.' for x in self.bools])

	def test_pot(self, pot):
		pot_bools = [
			pot.left.left.plant if pot.left and pot.left.left else False,
			pot.left.plant if pot.left else False,
			pot.plant,
			pot.right.plant if pot.right else False,
			pot.right.right.plant if pot.right and pot.right.right else False,
		]
		return pot_bools == self.bools


class Pot(object):
	def __init__(self, index, plant, rules):
		self.index = index
		self.plant = plant
		self.rules = rules
		self.left = None
		self.right = None
		self.next_plant = None

	def __repr__(self):
		return '#' if self.plant else '.'

	def set_next_plant(self):
		for r in self.rules:
			if r.test_pot(self):
				self.next_plant = r.outcome
				return
		self.next_plant = False

	def plant_next(self):
		self.plant = self.next_plant

	@property
	def value(self):
		return self.index if self.plant else 0


def is_plant(c):
	return True if c == '#' else False

def new_generation(pot):
	starter = pot
	while pot:
		pot.set_next_plant()
		pot = pot.right

	pot = starter
	while pot:
		pot.plant_next()
		pot = pot.right

def pot_value(pot):
	total = 0
	while pot:
		total += pot.value
		pot = pot.right
	return total

def potcount(pot, n):
	count = 0
	for i in range(abs(n)):
		if pot.plant:
			count += 1
		if n < 0:
			pot = pot.left
		else:
			pot = pot.right
	return count

def add_empty_pots(pot, n):
	for i in range(abs(n)):
		if n < 0:
			p = Pot(pot.index - 1, False, pot.rules)
			p.right = pot
			pot.left = p
			pot = p
		else:
			p = Pot(pot.index + 1, False, pot.rules)
			p.left = pot
			pot.right = p
			pot = p
	return pot

def print_pots(*args, **kwargs):
	print(generation_string(*args, **kwargs))

def generation_string(leftmost, generation):
	pot = leftmost
	plants = []
	while pot:
		plants.append(str(pot))
		pot = pot.right
	return "{:2d}: {}".format(generation, ''.join(plants))


def main(args):

	with open("input.txt", "r") as fh:
		file = fh.read()

# 	file = """
# 	initial state: #..#.#..##......###...###

# ...## => #
# ..#.. => #
# .#... => #
# .#.#. => #
# .#.## => #
# .##.. => #
# .#### => #
# #.#.# => #
# #.### => #
# ##.#. => #
# ##.## => #
# ###.. => #
# ###.# => #
# ####. => #
# 	"""

	initial_state = None
	rules = []
	input = file.strip().split("\n")
	for line in input:
		if line.strip() == '':
			continue
		mo = re.match(r'\s*initial state: ([\.\#]+)', line)
		if mo:
			initial_state = mo.group(1)
		else:
			mo = re.match(r'\s*([\.\#]+) => ([\.\#])', line)
			if not mo:
				print("Can't regex line: '{}'".format(line))
				exit(1)
			rules.append(Rule(mo.group(1), mo.group(2)))

	prev = None
	leftmost = None
	for i in range(len(initial_state)):
		p = Pot(i, True if initial_state[i] == '#' else False, rules)
		p.left = prev
		if p.left:
			p.left.right = p
		if i == 0:
			leftmost = p
		prev = p
	rightmost = prev

	generation_num = 20
	# plant_generations = [None for x in range(generation_num+1)]

	for g in range(generation_num+1):

		# For each generation, make sure we have enough extra on the left.
		if potcount(leftmost, 4):
			leftmost = add_empty_pots(leftmost, -5)
		if potcount(rightmost, -4):
			rightmost = add_empty_pots(rightmost, 5)

		if g != 0:
			new_generation(leftmost)

		# plant_generations[g] = generation_string(leftmost, generation=g)
		# print(plant_generations[g])

	total = pot_value(leftmost)
	print("Total for final generation = {}".format(total))


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	args = parser.parse_args()

	main(args)