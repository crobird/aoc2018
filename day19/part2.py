#!/usr/bin/env python


class Instruction(object):
	def __init__(self, line):
		bits = line.split(' ')
		self.opcode = bits[0]
		self.a = int(bits[1])
		self.b = int(bits[2])
		self.c = int(bits[3])

	def __repr__(self):
		return " ".join(map(str, [self.opcode, self.a, self.b, self.c]))

def addr(a, b, c, r):
	r[c] = r[a] + r[b]

def addi(a, b, c, r):
	r[c] = r[a] + b

def mulr(a, b, c, r):
	r[c] = r[a] * r[b]

def muli(a, b, c, r):
	r[c] = r[a] * b

def banr(a, b, c, r):
	r[c] = r[a] & r[b]

def bani(a, b, c, r):
	r[c] = r[a] & b

def borr(a, b, c, r):
	r[c] = r[a] | r[b]

def bori(a, b, c, r):
	r[c] = r[a] | r[b]

def setr(a, b, c, r):
	r[c] = r[a]

def seti(a, b, c, r):
	r[c] = a

def gtir(a, b, c, r):
	r[c] = 1 if a > r[b] else 0

def gtri(a, b, c, r):
	r[c] = 1 if r[a] > b else 0

def gtrr(a, b, c, r):
	r[c] = 1 if r[a] > r[b] else 0

def eqir(a, b, c, r):
	r[c] = 1 if a == r[b] else 0

def eqri(a, b, c, r):
	r[c] = 1 if r[a] == b else 0

def eqrr(a, b, c, r):
	r[c] = 1 if r[a] == r[b] else 0

OPCODE_MAP = dict(
	addr = addr,
	addi = addi,
	mulr = mulr,
	muli = muli,
	banr = banr,
	bani = bani,
	borr = borr,
	bori = bori,
	setr = setr,
	seti = seti,
	gtir = gtir,
	gtrr = gtrr,
	eqir = eqir,
	eqri = eqri,
	eqrr = eqrr
)

def print_registers(r):
	return ", ".join(map(str, r))

def main(args):
	with open(args.file, "r") as fh:
		input = fh.read()
	lines = input.split("\n")
	ins = []
	for line in lines:
		if line.startswith('#ip'):
			ip_bind = int(line.strip()[-1])
			continue
		ins.append(Instruction(line.strip()))

	# Wrong: 10551362
	registers = [1,0,0,0,0,0]
	ip = 0
	registers = [10551362, 10551361, 10501361, 8, 10551361, 0]
	#           [0, 3, 48652, 8, 10551361, 0]
	ip = 9
	i_count = 0
	seen = {}
	while True:
		if ip >= len(ins):
			# print("instruction {} out of bounds (len: {})".format(ip, len(ins)))
			break

		seen_str = "ip={} [{}]".format(ip, print_registers(registers))
		if seen_str in seen:
			print("{} was repeated on {}: {}".format(seen[seen_str], i_count, seen_str))
			break
		seen[seen_str] = i_count

		registers[ip_bind] = ip
		i = ins[ip]
		# print("Executing: {}".format(str(i)))
		# print_registers(registers)
		if i.opcode.startswith('gt'):
			print(seen_str + " " + str(i))
		else:
			pass
			# print("\t" + seen_str + " " + str(i))
		OPCODE_MAP[i.opcode](i.a, i.b, i.c, registers)
		# print_registers(registers)
		ip = registers[ip_bind]
		ip += 1
		i_count += 1
		if i_count == args.num:
			break

	print("Register 0 value is {}".format(registers[0]))





if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--file", help="file")
	parser.add_argument("-n", "--num", type=int, help="run n times")
	args = parser.parse_args()

	main(args)