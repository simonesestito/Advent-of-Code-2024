package main

import (
	"fmt"
	"bufio"
	"os"
	"log"
	"strings"
	"time"
)

/// Read the mapping input file, between graph nodes
/// and return a map of the graph (bidirectional)
func readInput(filename string) map[string]map[string]struct{} {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	graph := make(map[string]map[string]struct{})

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), "-")
		node1, node2 := line[0], line[1]

		// Add node1 -> node2
		if _, ok := graph[node1]; !ok {
			graph[node1] = make(map[string]struct{})
		}
		graph[node1][node2] = struct{}{}

		// Add node2 -> node1
		if _, ok := graph[node2]; !ok {
			graph[node2] = make(map[string]struct{})
		}
		graph[node2][node1] = struct{}{}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return graph
}

func countValidTriplets(graph map[string]map[string]struct{}) int {
	tripletsCount := 0

	// Iterate over all nodes...
	for node := range graph {
		// Since one of the nodes must start with T,
		// and all nodes of the triplet are interconnected,
		// we can filter out based on the starting letter, directly here, at the first step
		if node[0] != 't' {
			continue
		}

		// Find all nodes that are connected to the current node
		for secondStepNode := range graph[node] {
			// To avoid duplicates, if the second node starts with 't' as well,
			// ensure that it is lexicographically greater than the first node
			if secondStepNode[0] == 't' && secondStepNode <= node || node == secondStepNode {
				continue
			}

			// Find all nodes that are connected to the second step node
			for thirdStepNode := range graph[secondStepNode] {
				// To avoid triplet duplicates,
				// ensure that the third node is lexicographically greater than the second node
				if thirdStepNode <= secondStepNode {
					continue
				}

				// In case the third node starts with 't', then it must be greater than the first node too
				if thirdStepNode[0] == 't' && thirdStepNode <= node {
					continue
				}

				// If we can reach the first node from the third node, we have a triplet
				if _, ok := graph[thirdStepNode][node]; ok {
					// Finally, our triplet is valid if it contains at least one computer with a name that starts with "t"
					// We know that the first node starts with "t", so we are safe.
					tripletsCount++
				}
			}
		}
	}

	return tripletsCount
}


func runSolution(filename string) int {
	graph := readInput(filename)
	return countValidTriplets(graph)
}


func main() {
	testSolution := runSolution("aoc_23_example.txt")
	if testSolution != 7 {
		fmt.Println("Test failed! Expected 7, got", testSolution)
		return
	}
	fmt.Println("Test passed!")
	fmt.Println(runSolution("aoc_23.txt"))


	graph := readInput("aoc_23.txt")

	// Benchmark time!

	// Run 1000 times to warm up
	for i := 0; i < 1_000; i++ {
		countValidTriplets(graph)
	}

	// Run 50_000 times and measure the average time

	startTime := time.Now()
	for i := 0; i < 50_000; i++ {
		countValidTriplets(graph)
	}
	endTime := time.Now()
	fmt.Println("Duration:", endTime.Sub(startTime) / 50_000)
}
