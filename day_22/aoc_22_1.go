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


func generateFromSeed(seed uint32) uint64 {
	secret := uint64(seed)

	for i := 0; i < 2000; i++ {
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
	}

	return secret
}


func mix(result uint64, secret uint64) uint64 {
	return result ^ secret
}


func prune(x uint64) uint64 {
	return x & 16777215  // Last 24 bits
}


func sumGeneratedFromSeeds(seeds []uint32) uint64 {
	secrets := make(chan uint64, len(seeds))

	for _, seed := range seeds {
		go func(seed uint32) {
			secrets <- generateFromSeed(seed)
		}(seed)
	}


	total := uint64(0)

	for i := 0; i < len(seeds); i++ {
		total += <-secrets
	}

	return total
}


func main() {
	seeds := readInput("aoc_22.txt")
	allGenerated := sumGeneratedFromSeeds(seeds)
	fmt.Println(allGenerated)
}

