#!/usr/bin/env python

import re

class Node(object):
	def __init__(self, child_count, metadata_count):
		self.child_count = child_count
		self.metadata_count = metadata_count
		self.children = []
		self.metadata = []

	def __repr__(self):
		metadata = " - {}".format(" ".join([str(x) for x in self.metadata])) if self.metadata else ""
		return "{} {}{}".format(self.child_count, self.metadata_count, metadata)

	def metadata_sum(self):
		return sum(self.metadata)


class License(object):
	def __init__(self, input):
		self.input = input

	@property
	def size(self):
		return len(self.input)
	

	def take(self, n):
		v = []
		for i in range(n):
			v.append(self.input.pop(0))
		return v


def process_next_node(license, parent = None):
	lbits = license.take(2)
	if not lbits:
		return

	n = Node(*lbits)
	if parent:
		parent.children.append(n)

	# Look for child nodes
	for i in range(n.child_count):
		process_next_node(license, n)

	# Add metadata from license
	n.metadata = license.take(n.metadata_count)

	return n


def print_node(n, indent = 0):
	print("{}{}".format("   "*indent, n))
	for i in range(n.child_count):
		print_node(n.children[i], indent + 1)


def metadata_sum(n):
	total = n.metadata_sum()
	for i in range(n.child_count):
		total += metadata_sum(n.children[i])
	return total


with open("input.txt", "r") as fh:
	file = fh.read()

# file = """
# 2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
# """

input = file.strip().split("\n")
if len(input) > 1:
	print("Parsed more than one line!")
	exit(1)

input = input[0]

license = License([int(x) for x in input.split(' ')])

root = process_next_node(license)

print("Sum of all metadata: {}".format(metadata_sum(root)))
