#!/usr/bin/env python

import re

def can_go(step_list, step):
	return len([x for x in step.prereqs if x not in step_list]) == 0

def add_available_steps(step_list, steps, step):
	to_add = []
	for s in steps[step].after:
		if can_go(step_list, steps[s]):
			to_add.append(s)
	return to_add

class Step(object):
	def __init__(self, step):
		self.step = step
		self.prereqs = []
		self.after = []

	def __repr__(self):
		return "{} - prereq: {}, after: {}".format(self.step, ",".join(self.prereqs), ",".join(self.after))

	def add_prereq(self, prereq):
		self.prereqs.append(prereq)

	def add_after(self, step):
		self.after.append(step)


with open("input.txt", "r") as fh:
	file = fh.read()

# file = """
# Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.
# """

lines = file.split("\n")
steps = {}
for line in lines:
	if line == '':
		continue
	mo = re.match(r'Step (\w) must be finished before step (\w) can begin', line)
	if not mo:
		print("Couldn't parse line: {}".format(line))
		continue
	prereq = mo.group(1)
	step = mo.group(2)
	if step not in steps:
		steps[step] = Step(step)
	if prereq not in steps:
		steps[prereq] = Step(prereq)
	steps[step].add_prereq(prereq)
	steps[prereq].add_after(step)

available_steps = [x for x in steps if len(steps[x].prereqs) == 0]

step_list = []
remaining_steps = set(steps.keys())

while remaining_steps:
	if len(available_steps) == 0:
		print("Shouldn't have remaining steps with no available steps")
		exit(1)
	available_steps.sort()
	next_step = available_steps.pop(0)
	if next_step in step_list:
		continue
	step_list.append(next_step)
	remaining_steps.remove(next_step)
	available_steps.extend(add_available_steps(step_list, steps, next_step))

print('Step order: {}'.format("".join(step_list)))


