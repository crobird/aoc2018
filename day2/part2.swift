#!/usr/bin/swift

import Foundation

let textFile = try String(contentsOf: URL(fileURLWithPath: "input.txt")) 
let lines = textFile.split(separator: "\n")
let lineLength = lines[0].count
var commonWord:String?

for i in 0...lineLength {
	var s = Set<String>()
	for word in lines {
		var x = word
		let inx = word.index(word.startIndex, offsetBy:i)
		x.remove(at: inx)
		let subword = String(x)
		if s.contains(subword) {
			commonWord = subword
			break
		}
		s.insert(subword)
	}
	if commonWord != nil { break }
}

if commonWord != nil { 
	print("commonWord: \(commonWord!)")
}
