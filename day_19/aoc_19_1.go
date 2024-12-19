package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
	"strings"
)


func readInput(filename string) ([]string, []string) {
	file, err := os.Open(filename)
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }

	// Parse the first line
	stripes := strings.Split(lines[0], ", ")

	// The rest of the lines are okay as they are
	return stripes, lines[1:]
}


func optimizeStripes(stripes []string) map[byte][]string {
	stripesDict := make(map[byte][]string)

	// Index by the first letter
	for _, stripe := range stripes {
		letter := stripe[0]

		// Append to the list of stripes starting with that letter
		if prevStripes, exists := stripesDict[letter]; exists {
			stripesDict[letter] = append(prevStripes, stripe)
		} else {
			stripesDict[letter] = []string{stripe}
		}
	}

	return stripesDict
}


func solveDesigns(stripes map[byte][]string, designs []string) int {
	count := 0
	memoization := make(map[string]bool)
	for _, design := range designs {
		if solveDesign(stripes, design, memoization) {
			count++
		}
	}
	return count
}


func solveDesign(stripes map[byte][]string, design string, memoization map[string]bool) bool {
	// Base case: empty string
	if len(design) == 0 {
		return true
	}

	// Use cache
	if result, ok := memoization[design]; ok {
		return result
	}

	// Try with all stripes starting with the same letter
	char := design[0]
	if charStripes, ok := stripes[char]; ok {
		for _, stripe := range charStripes {
			if strings.HasPrefix(design, stripe) {
				// This is a potential candidate for solving the design
				nextDesign := design[len(stripe):]
				if solveDesign(stripes, nextDesign, memoization) {
					// Problem solved to the end!
					memoization[design] = true
					return true
				}
			}
		}
	}

	// No way to solve this design
	memoization[design] = false
	return false
}


func main() {
	stripes, designs := readInput("aoc_19.txt")
	stripesDict := optimizeStripes(stripes)

	result := solveDesigns(stripesDict, designs)
	fmt.Println(result)
}
