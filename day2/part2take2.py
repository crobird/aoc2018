#!/usr/bin/env python

def drop_char_at_index(s, i):
	if i == 0:
		return s[1:]
	elif i == len(s) - 1:
		return s[:-1]
	return s[:i-1] + s[i+1:]

with open("input.txt", "r") as fh:
	input = fh.read()

lines = input.split("\n")

stripped = [{} for i in range(len(lines[0]))]
for line in lines:
	for i in range(len(line)):
		newline = drop_char_at_index(line, i)
		if newline in stripped[i]:
			print("Found: {}".format(newline))
			exit(0)
		stripped[i][newline] = True

