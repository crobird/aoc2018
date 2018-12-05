#!/usr/bin/env python

def diff2(a,b):
	common = []
	for i in range(len(a)):
		if a[i] == b[i]:
			common.append(a[i])
	return common

with open("input.txt", "r") as fh:
	input = fh.read()

lines = input.split("\n")
for i in range(len(lines)):
	for j in range(len(lines)):
		if i == j or lines[i] == '' or lines[j] == '':
			continue
		common = diff2(lines[i], lines[j])
		if (len(lines[i]) - len(common) == 1):
			print("--")
			print(lines[i])
			print(lines[j])
			print(''.join(common))
			exit(1)
