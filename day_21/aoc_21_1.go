package main

import (
	"fmt"
	"strconv"
	"strings"
	"io"
	"os"
)


const MaxDepth = 300


func applyMove(move byte, i *uint8, j *uint8) {
	switch move {
	case 'v':
		(*i)++
	case '^':
		(*i)--
	case '>':
		(*j)++
	case '<':
		(*j)--
	default:
		panic("Invalid move to apply")
	}
}


type State struct {
	keypadI uint8
	keypadJ uint8

	robot1I uint8
	robot1J uint8

	robot2I uint8
	robot2J uint8
	
	output *[]byte
	validOutputI uint8

	depth uint16
}


func (s State) Hash() uint32 {
	// Custom hashing function
	hash := uint32(0)

	hash *= 12
	hash += uint32(s.keypadI * 3 + s.keypadJ)

	hash *= 6
	hash += uint32(s.robot1I * 3 + s.robot1J)

	hash *= 6
	hash += uint32(s.robot2I * 3 + s.robot2J)

	hash *= 5
	hash += uint32(s.validOutputI)

	hash *= uint32(MaxDepth + 1)
	hash += uint32(s.depth)

	return hash
}


func solvePin(pin string) uint32 {
	// Filter out empty strings
	if len(pin) == 0 {
		return uint32(0)
	}

	pinBytes := []byte(pin)

	state := State{
		keypadI: 3, keypadJ: 2,
		robot1I: 0, robot1J: 2,
		robot2I: 0, robot2J: 2,
		output: &pinBytes, validOutputI: uint8(0),
		depth: uint16(0),
	}

	states := make([]State, 0, 1000)
	states = append(states, state)

	visited := make(map[uint32]struct{}, 3000)

	bestSteps := [4]uint16{}

	// BFS
	for len(states) > 0 && states[0].validOutputI < uint8(len(*states[0].output)) {
		// Pop queue
		state = states[0]
		states = states[1:]

		if !state.Valid() {
			continue
		}

		bestStepsAtN := bestSteps[state.validOutputI]
		if bestStepsAtN > 0 && bestStepsAtN < state.depth {
			continue
		}

		// Skip duplicates
		hash := state.Hash()
		if _, exists := visited[hash]; exists {
			continue
		}
		visited[hash] = struct{}{}

		// Increase the depth
		state.depth++

		// Perform direction actions
		for _, action := range []byte("><^v") {
			newState := state  // Copy the state

			// Go in that direction
			applyMove(action, &newState.robot2I, &newState.robot2J)
			states = append(states, newState)
		}

		// Perform press button action (A)
		robot2 := arrow(state.robot2I, state.robot2J)
		if robot2 == 'A' {
			// Perform press button on robot 1
			robot1 := arrow(state.robot1I, state.robot1J)
			if robot1 == 'A' {
				// Perform press button on keypad (=> print)
				digit := getDigit(state.keypadI, state.keypadJ)
				if digit == (*state.output)[state.validOutputI] {
					bestSteps[state.validOutputI] = state.depth - 1
					state.validOutputI++
				} else {
					// Invalid PIN
					continue
				}
			} else {
				// Move keypad
				applyMove(robot1, &state.keypadI, &state.keypadJ)
			}
		} else {
			// Move robot 1
			applyMove(robot2, &state.robot1I, &state.robot1J)
		}

		states = append(states, state)
	}


	pinDigits, err := strconv.Atoi(pin[:3])
	if err != nil {
		panic(err)
	}
	sequenceLength := states[0].depth
	return uint32(sequenceLength) * uint32(pinDigits)
}


func arrow(i uint8, j uint8) byte {
	switch 3 * i + j {
	case 1:
		return '^'
	case 2:
		return 'A'
	case 3:
		return '<'
	case 4:
		return 'v'
	case 5:
		return '>'
	default:
		panic("Invalid arrow keypad position")
	}
}

func getDigit(i uint8, j uint8) byte {
	if i == 3 && j == 1 {
		return '0'
	} else if i == 3 && j == 2 {
		return 'A'
	}

	return byte('1' + 3*(2-i) + j)
}


func (s State) Valid() bool {
	if s.depth > MaxDepth {
		return false
	}

	if max(s.robot1I, s.robot2I) > 1 {
		return false
	}

	if s.keypadI > 3 {
		return false
	}

	if max(s.keypadJ, s.robot1J, s.robot2J) > 2 {
		return false
	}

	if s.keypadI == 3 && s.keypadJ == 0 {
		return false
	}

	if s.robot1I == 0 && s.robot1J == 0 {
		return false
	}

	if s.robot2I == 0 && s.robot2J == 0 {
		return false
	}

	return true
}


func solveAllPins(pins []string) uint32 {
	complexities := make(chan uint32, len(pins))

	for _, pin := range pins {
		go func(pin string) {
			complexities <- solvePin(pin)
		}(pin)
	}

	complexity := uint32(0)

	for _ = range pins {
		complexity += <-complexities
	}

	return complexity
}


func readInput(filename string) []string {
	// Basically, read all file lines

	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	allBytes, err := io.ReadAll(file)
	if err != nil {
		panic(err)
	}

	return strings.Split(string(allBytes), "\n")
}


func main() {
	pins := readInput("aoc_21.txt")
	complexity := solveAllPins(pins)
	fmt.Println(complexity)
}
