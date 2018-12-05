#!/usr/bin/env python

import re

# guard id -> {
	# events -> []
	# minutes -> count
# }

with open("input.txt", "r") as fh:
	file = fh.read()


lines = file.split("\n")
lines.sort()

guard_data = {}
current_guard = None
sleep_minute = None
for line in lines:
	if line == '':
		continue
	mo = re.match(r'\[(\d+)\-(\d+)\-(\d+)\s+(\d+):(\d+)\]\s+(.*)$', line)
	if mo:
		d = dict(
			year = int(mo.group(1)),
			month = int(mo.group(2)),
			day = int(mo.group(3)),
			hour = int(mo.group(4)),
			minute = int(mo.group(5)),
			event = mo.group(6)
		)
		mo2 = re.match(r'Guard #(\d+)\s', d['event'])
		if mo2:
			current_guard = mo2.group(1)
			if sleep_minute:
				print("Last guard never woke up!")
		elif d['event'] == 'wakes up':
			# Calculate last sleep minutes and log them
			count = 0
			for i in range(sleep_minute, d['minute']):
				guard_data[current_guard]['minutes'][i] += 1
				count += 1
			sleep_minute = None
		elif d['event'] == 'falls asleep':
			if sleep_minute:
				print("We fell asleep twice?!?")
			sleep_minute = d['minute']
		else:
			print("Missed an event: {}".format(d['event']))
		if current_guard not in guard_data:
			guard_data[current_guard] = dict(events=[], minutes=[0]*60)
		guard_data[current_guard]['events'].append(d)
	else:
		print("unexpected inability to parse line: {}".format(line))

max_minutes = 0
sleepy_guard = None
which_minute = None
for gid in guard_data:
	sleepiest_minute = None
	minute_count = 0
	for i, count in enumerate(guard_data[gid]['minutes']):
		if count > minute_count:
			sleepiest_minute = i
			minute_count = count
	if minute_count > max_minutes:
		sleepy_guard = gid
		which_minute = sleepiest_minute
		max_minutes = minute_count

print("Sleepiest minute was {} for {} minutes total (guard_id: {})".format(which_minute, max_minutes, sleepy_guard))

print("answer: {}".format(int(sleepy_guard) * which_minute))