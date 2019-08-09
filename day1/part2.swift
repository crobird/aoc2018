#!/usr/bin/swift

import Foundation

let textFile = try String(contentsOf: URL(fileURLWithPath: "input.txt")) 
let lines = textFile.split(separator: "\n")

var total = 0
var seenTotals = Set<Int>()
var dupe: Int?

while true {
	for line in lines {
		if let i = Int(line) {
			total += i
			if seenTotals.contains(total) {
				dupe = total
				break
			}
			seenTotals.insert(total)
		}
	}
	if dupe != nil { break }
}

print("First duplicate total: \(dupe!)")
