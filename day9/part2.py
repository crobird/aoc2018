#!/usr/bin/env python

import re


class Marble(object):
	def __init__(self, v, prev_marble = None, next_marble = None):
		self.value = v
		self.prev  = prev_marble if prev_marble else self
		self.next  = next_marble if next_marble else self

	def __repr__(self):
		return str(self.value)

class Marbles(object):
	def __init__(self, player_count, marble_count):
		self.current = Marble(0)
		self.total_marbles = marble_count
		self.players = [0 for i in range(player_count)]
		self.current_player = 0
		self.next = 1

		print("Creating a game with marble_count={}, player_count={}".format(marble_count, player_count))

	def __repr__(self):
		m = self.current
		l = ["({})".format(m.value)]
		m = m.next
		while m != self.current:
			l.append(str(m.value))
			m = m.next

		return "[{}] {}".format(self.current_player if len(self.in_play) != 1 else "-",
			" ".join(l))

	def get_next(self):
		if self.next < self.total_marbles:
			next_value = self.next
			self.next += 1
			return next_value
		else:
			return None

	def is_special(self, marble):
		if marble % 23 == 0:
			return True
		return False

	def score(self, add_value):
		self.players[self.current_player] += add_value

	def place_marble(self, marble):
		plus_one = self.current.next
		plus_two = plus_one.next
		m = Marble(marble, prev_marble = plus_one, next_marble = plus_two)
		plus_one.next = m
		plus_two.prev = m
		self.current = m

	def get_prev_marble(self, n = 1):
		m = self.current
		for i in range(n):
			m = m.prev
		return m

	def next_turn(self):
		marble = self.get_next()
		if not marble:
			return

		if self.is_special(marble):
			self.score(marble)
			seven_back = self.get_prev_marble(7)
			self.score(seven_back.value)

			# Remove 7 back and reset current
			before_seven = seven_back.prev
			before_seven.next = seven_back.next
			seven_back.next.prev = before_seven
			self.current = before_seven.next
		else:
			self.place_marble(marble)

		self.current_player = (self.current_player + 1) % len(self.players)
		return True

	@property
	def highest_score(self):
		return max(self.players)
	

	def run(self):
		while True:
			if not self.next_turn():
				break

		print("Highest score is {}".format(self.highest_score))


with open("input.txt", "r") as fh:
	file = fh.read()

# file = """
# 13 players; last marble is worth 7999 points
# """

input = file.strip().split("\n")
mo = re.match(r'(\d+) players; last marble is worth (\d+) points', input[0])
if not mo:
	print("Can't regex line")
	exit(1)

m = Marbles(int(mo.group(1)), (int(mo.group(2))*100) - 1)
m.run()

