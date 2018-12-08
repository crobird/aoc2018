#!/usr/bin/env python

import re

def step_cost(step, base_time=0):
	return ord(step) - 64 + base_time

def can_go(step_list, step):
	return len([x for x in step.prereqs if x not in step_list]) == 0

def add_available_steps(available_steps, step_list, steps, step):
	to_add = []
	for s in steps[step].after:
		if can_go(step_list, steps[s]) and s not in available_steps:
			to_add.append(s)
	available_steps.extend(to_add)

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
worker_count = 5
base_cost = 60
workers = [None for i in range(worker_count)]
total_seconds = 0
elapsed_time = 0

while remaining_steps:
	# if len(available_steps) == 0:
	# 	print("Shouldn't have remaining steps with no available steps")
	# 	exit(1)

	if available_steps:
		available_steps.sort()

	available_workers = []
	for i,v in enumerate(workers):
		if not v:
			available_workers.append(i)
			continue

		# Reduce remaining time for each workers job
		workers[i] = (v[0], v[1] - elapsed_time)

	# Assign available jobs to available workers
	while available_workers and available_steps:
		next_step = available_steps.pop(0)
		next_worker = available_workers.pop(0)
		workers[next_worker] = (next_step, step_cost(next_step, base_cost))

	for i,v in enumerate(workers):
		if not v:
			continue
		print("\t{}: {}".format(v[0], v[1]))

	# Find next worker(s) to be done
	shortest_time = min([x[1] for x in workers if x is not None])
	for i,v in enumerate(workers):
		if v is None:
			continue
		(s,t) = v
		if t == shortest_time:
			step_list.append(s)
			remaining_steps.remove(s)
			add_available_steps(available_steps, step_list, steps, s)
			workers[i] = None

	total_seconds += shortest_time
	elapsed_time = shortest_time

print('Step order: {} in {} seconds'.format("".join(step_list), total_seconds))


