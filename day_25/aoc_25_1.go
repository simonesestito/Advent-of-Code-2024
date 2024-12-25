package main

import (
	"fmt"
	"os"
	"bufio"
)


type Heights [5]uint8


func readInput(filename string) ([]Heights, []Heights) {
	// Store keys and locks heights
	keys := make([]Heights, 0, 250)
	locks := make([]Heights, 0, 250)

	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(file)

	// We have 7 lines, representing a key or a lock,
	// interleaved with an empty line
	for scanner.Scan() {
		// The first line tells us whether it's a key or a lock
		isLock := scanner.Text()[0] == '#'
		
		// Read 5 lines, that represent the heights
		heights := Heights{}
		for i := 0; i < 5; i++ {
			scanner.Scan()
			line := scanner.Text()
			for j, char := range line {
				if char == '#' {
					heights[j]++
				}
			}
		}

		// Skip the last line
		// It is a sequence of # or .,
		// depending if it is a lock or a key
		scanner.Scan()

		// Also skip the empty interleaving line
		scanner.Scan()

		if isLock {
			locks = append(locks, heights)
		} else {
			keys = append(keys, heights)
		}
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}

	return keys, locks
}


func tryCombination(key Heights, lock Heights) bool {
	for i := range key {
		if key[i] + lock[i] > 5 {
			return false
		}
	}

	return true
}


func tryKey(key Heights, locks []Heights) uint16 {
	var count uint16

	for _, lock := range locks {
		if tryCombination(key, lock) {
			count++
		}
	}

	return count
}


func tryAll(keys []Heights, locks []Heights) uint16 {
	var total uint16
	for _, key := range keys {
		total += tryKey(key, locks)
	}
	return total
}


func main() {
	keys, locks := readInput("aoc_25.txt")
	result := tryAll(keys, locks)
	fmt.Println(result)
}
