package main

import (
	"fmt"
	"strconv"
	"os"
	"bufio"
	"strings"
)


type Gate struct {
	x *Gate
	y *Gate
	
	processingFunc func(x uint8, y uint8) uint8

	previousOutput uint8
	hasOutput bool
}

func (g *Gate) Output(m *GatesMap) uint8 {
	if !g.hasOutput && g.processingFunc != nil {
		x := g.x.Output(m)
		y := g.y.Output(m)
		g.previousOutput = g.processingFunc(x, y)
		g.hasOutput = true
	}
	return g.previousOutput
}


func OrGate(x uint8, y uint8) uint8 {
	return x | y
}


func AndGate(x uint8, y uint8) uint8 {
	return x & y
}


func XorGate(x uint8, y uint8) uint8 {
	return x ^ y
}


type GatesMap struct {
	gates [15_848]Gate  // 23*26*26 for normal gates + 300 for xyz special gates
}

func hashGateName(name string) uint16 {
	// Special cases: x, y, z
	if name[0] == 'x' || name[0] == 'y' || name[0] == 'z' {
		shift := uint16(name[0] - 'x') * 100
		digits, err := strconv.Atoi(name[1:])
		if err != nil {
			panic(err)
		}
		return shift + uint16(digits)
	}

	// Normal alphabetic gates
	var hash uint16
	for i := 0; i < 3; i++ {
		hashPart := uint16(name[i] - 'a')
		if hashPart < 0 || hashPart > 25 {
			panic("Error hash")
		}
		
		hash = hash * 26 + hashPart
	}

	return hash + 300
}


func (m *GatesMap) Get(name string) *Gate {
	hash := hashGateName(name)
	return &m.gates[hash]
}


func (m *GatesMap) PutValue(name string, value uint8) {
	gate := m.Get(name)
	gate.x = nil
	gate.y = nil
	gate.previousOutput = value
	gate.hasOutput = true
}


func (m *GatesMap) PutFunc(name string, x string, y string, opName string) {
	var op func(x, y uint8) uint8
	if opName == "AND" {
		op = AndGate
	} else if opName == "OR" {
		op = OrGate
	} else if opName == "XOR" {
		op = XorGate
	} else {
		panic(opName)
	}

	gate := m.Get(name)
	gate.x = m.Get(x)
	gate.y = m.Get(y)
	gate.previousOutput = 0
	gate.hasOutput = false
	gate.processingFunc = op
}


func readInput(filename string) *GatesMap {
	gates := &GatesMap{}

	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}

	scan := bufio.NewScanner(file)
	
	// Read the first input lines, until a double line break
	for scan.Scan() {
		line := scan.Text()
		if len(line) == 0 {
			// Go parsing the gates
			break
		}

		// Parse the input gates (values)
		lineParts := strings.Split(line, ": ")
		gateName := lineParts[0]
		value, err := strconv.Atoi(lineParts[1])
		if err != nil {
			panic(err)
		}
		gates.PutValue(gateName, uint8(value))
	}

	// Read the gates
	for scan.Scan() {
		line := scan.Text()

		var x, op, y, z string
		if _, err := fmt.Sscanf(line, "%s %s %s -> %s", &x, &op, &y, &z); err != nil {
			panic(err)
		}

		gates.PutFunc(z, x, y, op)
	}

	if err := scan.Err(); err != nil {
		panic(err)
	}

	return gates
}


func getOutputNumber(gates *GatesMap) uint {
	var outputNumber uint

	for i := 99; i >= 0; i-- {
		name := fmt.Sprintf("z%02d", i)
		bit := gates.Get(name).Output(gates)
		outputNumber = outputNumber * 2 + uint(bit)
	}

	return outputNumber
}


func main() {
	gates := readInput("aoc_24.txt")
	solution := getOutputNumber(gates)
	fmt.Println(solution)
}

