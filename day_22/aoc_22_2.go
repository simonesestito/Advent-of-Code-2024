package main

import (
	"fmt"
	"os"
	"bufio"
	"strconv"
)


func readInput(filename string) []uint32 {
	// Read a list of integers, basically
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}

	numbers := []uint32{}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		number, err := strconv.Atoi(line)
		if err != nil {
			panic(err)
		}
		numbers = append(numbers, uint32(number))
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}

	return numbers
}


// Map every 4-length sequence into an array of 2020 items
// each one having the result for that sequence, for any seed
type PriceDiff map[[4]int8]uint16


func generateFromSeed(seed uint32, allDiffs PriceDiff) {
	secret := uint64(seed)

	price := uint8(secret % 10)
	priceDiffs := [4]int8{}

	for i := uint16(0); i < 2000; i++ {
		// Generate the next one
		result := secret << 6
		secret = mix(result, secret)
		secret = prune(secret)

		result = secret >> 5
		secret = mix(result, secret)
		secret = prune(secret)

		result = secret << 11
		secret = mix(result, secret)
		secret = prune(secret)

		// Compute price and diff
		newPrice := uint8(secret % 10)
		priceDiff := int8(newPrice) - int8(price)
		price = newPrice

		priceDiffs = [4]int8(append(priceDiffs[1:], priceDiff))
	
		if i >= 3 {
			if _, exists := allDiffs[priceDiffs]; !exists {
				allDiffs[priceDiffs] = uint16(price)
			}
		}
	}
}


func mix(result uint64, secret uint64) uint64 {
	return result ^ secret
}


func prune(x uint64) uint64 {
	return x & 16777215  // Last 24 bits
}


func findBestSequenceForSeeds(seeds []uint32) uint16 {
	allDiffs := make([]PriceDiff, len(seeds))
	doneSignal := make(chan struct{}, len(seeds))

	for i, seed := range seeds {
		allDiffs[i] = make(PriceDiff)
		go func(seed uint32, diffs PriceDiff) {
			generateFromSeed(seed, diffs)
			doneSignal <- struct{}{}
		}(seed, allDiffs[i])
	}

	for i := 0; i < len(seeds); i++ {
		<-doneSignal
	}

	// Joining diffs
	globalDiff := make(PriceDiff)
	for _, seedDiff := range allDiffs {
		for sequence, price := range seedDiff {
			globalDiff[sequence] += price
		}
	}

	maxTotal := uint16(0)
	for _, total := range globalDiff {
		if total > maxTotal {
			maxTotal = total
		}
	}
	return maxTotal

	/*

	maxDiff := intersectPriceDiffs(allDiffs)
	fmt.Println()
	fmt.Printf("%#v\n", maxDiff)
	return maxDiff.total

	*/
}


func main() {
	seeds := readInput("aoc_22.txt")
	maxTotal := findBestSequenceForSeeds(seeds)
	fmt.Println(maxTotal)
}

