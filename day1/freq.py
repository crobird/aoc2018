#!/usr/bin/env python

sum = 0
sums = {}
with open("input.txt", "r") as fh:
	lines = fh.read()

while(True):	
	print("looping....")
	for line in lines.split("\n"):
		if line == '':
			continue
		x = int(line)
		sum += x
		if sum not in sums:
			sums[sum] = 1
		else:
			print("Just saw sum {} again".format(sum))
			exit(0)

print(sum)