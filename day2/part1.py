#!/usr/bin/env python


with open("input.txt", "r") as fh:
	lines = fh.read()

twice = 0
three = 0
for line in lines.split("\n"):
	lets = {}
	if line == '':
		continue
	for x in line:
		if x not in lets:
			lets[x] = 1
		else:
			lets[x] += 1

	if any([lets[x] == 2 for x in lets]):
		twice += 1

	if any([lets[x] == 3 for x in lets]):
		three += 1


print("twice: {}, three: {}, checksum: {}".format(twice, three, twice*three))
