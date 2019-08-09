#!/usr/bin/swift

import Foundation

let textFile = try String(contentsOf: URL(fileURLWithPath: "input.txt")) 
let lines = textFile.split(separator: "\n")

var total = 0
for line in lines {
	if let i = Int(line) {
		total += i
	}
}

print("Final total: \(total)")
