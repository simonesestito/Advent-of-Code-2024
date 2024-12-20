package main

import (
	"fmt"
	"log"
	"os"
	"bufio"
)


type Grid struct {
	rows  int
	cols  int
	cells [][]byte
}

func initGrid(rows int, cols int) *Grid {
	cells := make([][]byte, rows)
	for i := range cells {
		cells[i] = make([]byte, cols)
	}

	return &Grid{
		rows: rows,
		cols: cols,
		cells: cells,
	}
}

func (g *Grid) get(i int, j int) byte {
	// Fill out-of-bounds cells with a default value
	if i < 0 || i >= g.rows || j < 0 || j >= g.cols {
		return '#'
	}

	return g.cells[i][j]
}


func (g *Grid) getPoint(point Point) byte {
	return g.get(point.i, point.j)
}


func readInput(filename string) *Grid {
	file, err := os.Open(filename)
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(file)

	// First line to initialize the grid
	scanner.Scan()
	line := scanner.Text()
	grid := initGrid(len(line), len(line))
	
	for j, cell := range []byte(line) {
		grid.cells[0][j] = cell
	}

	
	// Continue with the next lines
	i := 1
	for scanner.Scan() {
		line := scanner.Text()
		for j, cell := range []byte(line) {
			grid.cells[i][j] = cell
		}
		i++
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	return grid
}


type Point struct {
	i 	  int
	j 	  int
}

type Node struct {
	point Point
	score int
	prev  *Node
}


func (g *Grid) findPoint(value byte) Point {
	for i, row := range g.cells {
		for j, cell := range row {
			if cell == value {
				return Point{i:i, j:j}
			}
		}
	}

	return Point{-1,-1}
}


func bfs(grid *Grid) map[Point]int {
	var queue []Node
	scores := make(map[Point]int)

	// Add the end point (start BFS from the end)
	// start := grid.findPoint('S')
	end := grid.findPoint('E')

	queue = append(queue, Node{point: end, prev: nil})

	for len(queue) > 0 {
		// Pop
		node := queue[0]
		queue = queue[1:]

		// Check if visited
		if _, exists := scores[node.point]; exists {
			continue
		}

		// Compute my score
		if node.prev == nil {
			node.score = 1
		} else {
			node.score = node.prev.score + 1
		}

		scores[node.point] = node.score

		// Go to my neighbours
		directions := []Point{ {0,1}, {0,-1}, {1,0}, {-1,0} }
		for _, direction := range directions {
			i, j := node.point.i, node.point.j
			nextI, nextJ := i + direction.i, j + direction.j

			// Don't visit walls
			if grid.get(nextI, nextJ) != '#' {
				// Visit my valid neighbour
				nextNode := Node{
					point: Point{i: nextI, j: nextJ},
					prev: &node,
				}
				queue = append(queue, nextNode)
			}
		}
	}

	// Now, every node has its minimum distance to the end
	return scores
}


func isValidCheat(grid *Grid, scores map[Point]int, from Point, diff Point) bool {
	i, j := from.i, from.j
	cell := grid.cells[i][j]

	// We only want walls
	if cell != '#' {
		return false
	}

	// We want neighbours not to be walls,
	// because this wall must be only 1 cell thick
	topPoint := Point{i: i - diff.i, j: j - diff.j}
	topCell := grid.getPoint(topPoint)

	bottomPoint := Point{i: i + diff.i, j: j + diff.j}
	bottomCell := grid.getPoint(bottomPoint)

	if topCell == '#' || bottomCell == '#' {
		return false
	}

	// Compute their scores difference
	// It must be at least 100
	scoresDiff := scores[topPoint] - scores[bottomPoint]
	if scoresDiff < 0 {
		scoresDiff = -scoresDiff
	}

	return scoresDiff > 100  // +1 which is the wall cell
}


func countCheats(grid *Grid) int {
	scores := bfs(grid)

	// See the grid, and count walls that:
	// - are 1 cell thick
	// - the difference of scores of neighbours is >= 100

	count := 0

	for i, row := range grid.cells {
		for j := range row {
			// Check this wall
			if isValidCheat(grid, scores, Point{i, j}, Point{1, 0}) {
				count++
			}

			if isValidCheat(grid, scores, Point{i, j}, Point{0, 1}) {
				count++
			}
		}
	}

	return count
}


func main() {
	grid := readInput("aoc_20.txt")

	cheats := countCheats(grid)
	fmt.Println(cheats)
}
