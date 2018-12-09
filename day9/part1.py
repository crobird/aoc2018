#!/usr/bin/env python

import re



class Marbles(object):
	def __init__(self, player_count, marble_count):
		self.in_play = [0]
		self.current = 0
		self.total_marbles = marble_count
		self.players = [0 for i in range(player_count)]
		self.next = 1
		self.current_player = 0

		print("Creating a game with marble_count={}, player_count={}".format(marble_count, player_count))

	def __repr__(self):
		return "[{}] {} [[{}]]".format(self.current_player if len(self.in_play) != 1 else "-",
			" ".join([str(m) if self.current != i else "({})".format(m) for i,m in enumerate(self.in_play)]),
			len(self.in_play))

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

	def place_marble(self, marble):
		new_index = self.get_c_index(2)
		self.in_play.insert(new_index, marble)
		self.current = new_index

	def get_c_index(self, n):
		# special case for the beginning
		if len(self.in_play) == 1:
			return 1

		new_index = (self.current + n) % len(self.in_play)
		return (self.current + n) % len(self.in_play)

	def get_cc_index(self, n):
		new_index = self.current - n
		while new_index < 0:
			new_index = len(self.in_play) + new_index
		return new_index

	def score(self, add_value):
		self.players[self.current_player] += add_value

	def next_turn(self):
		marble = self.get_next()
		if not marble:
			return

		if self.is_special(marble):
			self.score(marble)
			cc_index = self.get_cc_index(7)
			self.score(self.in_play[cc_index])
			self.in_play.pop(cc_index)
			self.current = cc_index % len(self.in_play)
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

m = Marbles(int(mo.group(1)), int(mo.group(2)) - 1)
m.run()

