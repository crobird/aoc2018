#!/usr/bin/swift

import Foundation

let textFile = try String(contentsOf: URL(fileURLWithPath: "input.txt")) 
let lines = textFile.split(separator: "\n")

var twos   = 0
var threes = 0
for line in lines {
	var hasTwo = false
	var hasThree = false
	var freq = [Character:Int]()
	for c in line {
		if c >= "a" && c <= "z" { 
			if let ov = freq[c] { freq[c] = ov + 1 }
			else { freq[c] = 1 }
		}
	}
	for (_,f) in freq {
		if f == 2 { hasTwo = true }
		else if f == 3 { hasThree = true }
		if hasTwo && hasThree { break }
	}
	if hasTwo { twos += 1 }
	if hasThree { threes += 1 }
}
let checksum = twos * threes
print("checksum: \(checksum)")

