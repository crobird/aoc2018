#!/usr/bin/env python

import re
import enum

class RoadType(enum.Enum):
	INTERSECTION      = 1
	VERTICAL          = 2
	HORIZONTAL        = 3
	CORNER_RIGHT_DOWN = 4
	CORNER_RIGHT_UP   = 5
	CORNER_LEFT_DOWN  = 6
	CORNER_LEFT_UP    = 7

CORNERS = [RoadType.CORNER_RIGHT_DOWN, RoadType.CORNER_RIGHT_UP, RoadType.CORNER_LEFT_DOWN, RoadType.CORNER_LEFT_UP]

ROAD_CHARS = {
	RoadType.INTERSECTION: '+',     
	RoadType.VERTICAL: '|',         
	RoadType.HORIZONTAL: '-',       
	RoadType.CORNER_RIGHT_DOWN: '/',
	RoadType.CORNER_RIGHT_UP: '\\',  
	RoadType.CORNER_LEFT_DOWN: '\\', 
	RoadType.CORNER_LEFT_UP: '/'   
}

def getRoadType(c, prev_char, next_char):
	horizontal_connectors = ['-', '+', '<', '>']
	vertical_connectors   = ['|', '+', 'v', '^']
	if c == '+':
		return RoadType.INTERSECTION
	if c == '|':
		return RoadType.VERTICAL
	if c == '-':
		return RoadType.HORIZONTAL
	if c == '/' and prev_char in horizontal_connectors:
		return RoadType.CORNER_LEFT_UP
	if c == '/' and next_char in horizontal_connectors:
		return RoadType.CORNER_RIGHT_DOWN
	if c == '\\' and next_char in horizontal_connectors:
		return RoadType.CORNER_RIGHT_UP
	if c == '\\' and prev_char in horizontal_connectors:
		return RoadType.CORNER_LEFT_DOWN
	if c == '>' or c == '<':
		return RoadType.HORIZONTAL
	if c == '^' or c == 'v':
		return RoadType.VERTICAL
	print("ERROR: INVALID ROAD TYPE - '{}', ('{}'), '{}'".format(prev_char, c, next_char))

class CarType(enum.Enum):
	EAST  = 1
	WEST  = 2
	NORTH = 3
	SOUTH = 4

CAR_TYPES = {
	CarType.EAST:  '>',
	CarType.WEST:  '<',
	CarType.NORTH: '^',
	CarType.SOUTH: 'v'
}

def getCarType(c):
	if c == 'v':
		return CarType.SOUTH
	if c == '^':
		return CarType.NORTH
	if c == '<':
		return CarType.WEST
	if c == '>':
		return CarType.EAST

class CarMove(enum.Enum):
	LEFT = 1
	STRAIGHT = 2
	RIGHT = 3

NEXT_MOVE_MAP = {
	CarType.SOUTH: { CarMove.LEFT: CarType.EAST,  CarMove.RIGHT: CarType.WEST  },
	CarType.NORTH: { CarMove.LEFT: CarType.WEST,  CarMove.RIGHT: CarType.EAST  },
	CarType.EAST:  { CarMove.LEFT: CarType.NORTH, CarMove.RIGHT: CarType.SOUTH },
	CarType.WEST:  { CarMove.LEFT: CarType.SOUTH, CarMove.RIGHT: CarType.NORTH }
}

CORNER_MAP = {
	CarType.SOUTH: { RoadType.CORNER_RIGHT_UP:   CarType.EAST,  RoadType.CORNER_LEFT_UP:   CarType.WEST   },
	CarType.NORTH: { RoadType.CORNER_RIGHT_DOWN: CarType.EAST,  RoadType.CORNER_LEFT_DOWN: CarType.WEST   },
	CarType.EAST:  { RoadType.CORNER_LEFT_UP:    CarType.NORTH, RoadType.CORNER_LEFT_DOWN: CarType.SOUTH  },
	CarType.WEST:  { RoadType.CORNER_RIGHT_DOWN: CarType.SOUTH, RoadType.CORNER_RIGHT_UP:   CarType.NORTH }
}

class Car(object):
	# move here means intersection, not vehicle movement
	def __init__(self, c):
		self.car_type = getCarType(c)
		self.last_move = None

	def __repr__(self):
		return CAR_TYPES[self.car_type]

	def next_car_type_for_intersection(self, move):
		if move == CarMove.STRAIGHT:
			return self.car_type
		return NEXT_MOVE_MAP[self.car_type][move]

	def next_move(self):
		if not self.last_move or self.last_move == CarMove.RIGHT:
			self.last_move = CarMove.LEFT
		elif self.last_move == CarMove.STRAIGHT:
			self.last_move = CarMove.RIGHT
		else:
			self.last_move = CarMove.STRAIGHT
		self.car_type = self.next_car_type_for_intersection(self.last_move)
		return self.last_move

	def handle_corner(self, road_type):
		self.car_type = CORNER_MAP[self.car_type][road_type]

class Road(object):
	def __init__(self, x, y, c, prev_char, next_char):
		self.x = x
		self.y = y
		self.car = Car(c) if c in ['v','<','>','^'] else None
		self.road_type  = getRoadType(c, prev_char, next_char)
		if not self.road_type:
			print("Error at {},{}".format(self.x, self.y))

	def __repr__(self):
		return str(self.car) if self.car else ROAD_CHARS[self.road_type]


def order_cars(cars, mult):
	return sorted(cars, key=lambda a: (a[1] * mult) + a[0])

def get_next_car_move(track, x, y):
	c = track[y][x].car
	if c.car_type == CarType.SOUTH:
		return (x,y+1)
	if c.car_type == CarType.NORTH:
		return (x,y-1)
	if c.car_type == CarType.EAST:
		return (x+1,y)
	if c.car_type == CarType.WEST:
		return (x-1,y)

def dump_track(track):
	lines = []
	for i in range(len(track)):
		line = []
		for j in range(len(track[0])):
			r = track[i][j]
			line.append(str(r) if r else ' ')
		lines.append(''.join(line))
	return "\n".join(lines)


def main(args):

	with open("input.txt", "r") as fh:
	# with open("sample.txt", "r") as fh:
		file = fh.read()

	input = file.split("\n")
	max_line_length = max([len(x) for x in input])
	track = [[None for x in range(max_line_length)] for y in range(len(input))]
	cars = []
	for i in range(len(input)):
		line = input[i]
		if line.strip() == '':
			continue
		for j in range(len(line)):
			if line[j] == ' ':
				continue
			prev_char = line[j-1] if j != 0 else None
			next_char = line[j+1] if j < len(line) - 1 else None
			r = Road(j, i, line[j], prev_char, next_char)
			if r.car:
				cars.append((j,i))
			track[i][j] = r

	ordering_mult = len(str(len(track))) * 10
	while True:
		car_order = order_cars(cars, ordering_mult)
		cars = []
		for x,y in car_order:
			next_x, next_y = get_next_car_move(track, x, y)
			next_road = track[next_y][next_x]
			try:
				car = track[y][x].car
				if next_road.car:
					print("Collision at {},{}".format(next_x, next_y))
					exit(0)
				if next_road.road_type == RoadType.INTERSECTION:
					car.next_move()
				elif next_road.road_type in CORNERS:
					car.handle_corner(next_road.road_type)
				next_road.car = car
				track[y][x].car = None
				cars.append((next_x,next_y))
			except Exception as e:
				print("Got exception: {}".format(e))
				with open("out.txt", "w") as fh:
					fh.write(dump_track(track))
				exit(1)



if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	args = parser.parse_args()

	main(args)