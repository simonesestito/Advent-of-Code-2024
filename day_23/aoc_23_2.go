package main

import (
	"fmt"
	"bufio"
	"os"
	"log"
	"strings"
	"sort"
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

type Clique map[string]struct{}  // set of nodes

type Graph map[string]map[string]struct{}  // adjacency list


func findBiggestConnectedGraph(graph Graph) Clique {
	r := make(Clique)
	p := make([]string, 0, len(graph))
	x := make([]string, 0)

	// P must contain all nodes
	for node := range graph {
		p = append(p, node)
	}

	maxKnownClique := make(Clique)
	bronKerbosch(graph, r, p, x, &maxKnownClique)
	return maxKnownClique
}


func bronKerbosch(graph Graph, r Clique, p []string, x []string, maxKnownClique *Clique) {
	// If both p and x are empty, we have found a maximal clique
	if len(p) == 0 && len(x) == 0 {
		if len(r) > len(*maxKnownClique) {
			// This is a new maximal clique, even bigger than the best previous ones
			rCopy := make(Clique, len(r))
			for vertex := range r {
				rCopy[vertex] = struct{}{}
			}
			*maxKnownClique = rCopy
		}
		return
	}

	// If the current clique is smaller than the best known one, we can stop
	if len(r) + len(p) <= len(*maxKnownClique) {
		// We cannot do better than the best known clique
		return
	}

	for i, vertex := range p {
		// Create a new set of r, p, x
		adjacencyList := graph[vertex]

		// R' = R union {vertex}
		r[vertex] = struct{}{}

		// P' = P intersect Neighbours(vertex)
		truncatedP := p[i+1:]  // First, consider P without previous vertices
		newP := make([]string, 0, min(len(truncatedP), len(graph[vertex])))
		for _, pVertex := range truncatedP {
			if _, isNeighbour := adjacencyList[pVertex]; isNeighbour {
				newP = append(newP, pVertex)
			}
		}

		// X' = X intersect Neighbours(vertex)
		newX := make([]string, 0, min(len(x), len(graph[vertex])) + 1)
		for _, xVertex := range x {
			if _, isNeighbour := adjacencyList[xVertex]; isNeighbour {
				newX = append(newX, xVertex)
			}
		}

		// Recursively call the bronKerbosch algorithm
		bronKerbosch(graph, r, newP, newX, maxKnownClique)

		// Add the vertex to X
		x = append(x, vertex)

		// Restore old R
		delete(r, vertex)
	}
}


func getPassword(graph map[string]map[string]struct{}) string {
	maxKnownClique := findBiggestConnectedGraph(graph)

	// Collect the nodes in the maximal clique
	nodes := make([]string, 0, len(maxKnownClique))
	for node := range maxKnownClique {
		nodes = append(nodes, node)
	}

	// Sort the nodes lexicographically
	sort.Strings(nodes)

	// The password is the comma-separated list of nodes
	return strings.Join(nodes, ",")
}


func runSolution(filename string) string {
	graph := readInput(filename)
	return getPassword(graph)
}


func main() {
	testSolution := runSolution("aoc_23_example.txt")
	if testSolution != "co,de,ka,ta" {
		fmt.Println("Test failed! Expected 7, got", testSolution)
		return
	}
	fmt.Println("Test passed!")

	fmt.Println(runSolution("aoc_23.txt"))

	graph := readInput("aoc_23.txt")

	// Benchmark time!

	// Run 100 times to warm up
	for i := 0; i < 100; i++ {
		getPassword(graph)
	}

	// Run 500 times and measure the average time
	iterations := 500
	fmt.Println("Running", iterations, "iterations...")

	startTime := time.Now()
	for i := 0; i < iterations; i++ {
		getPassword(graph)
	}
	endTime := time.Now()
	fmt.Println("Duration:", endTime.Sub(startTime) / time.Duration(iterations))
}
