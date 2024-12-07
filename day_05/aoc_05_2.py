'''
Idea:
- every update is the set of nodes of a graph
- the rules corresponding to the nodes of an update are the edges of the graph
- a valid update is the topological order of the graph
'''

from collections import deque
from typing import Generator
from aoc_05_utils import Rules, Update, read_input, test_valid_update


def topological_sort(vertices: Update, edges: Rules, max_n) -> Update:
    # Step 1: Calculate in-degrees
    in_degree = [0] * max_n
    for i in vertices:
        for j in vertices:
            if j in edges[i]:
                in_degree[j] += 1

    # Step 2: Initialize queue with vertices of in-degree 0
    queue = deque([i for i in vertices if in_degree[i] == 0])
    topological_order: Update = []

    while queue:
        current = queue.popleft()
        topological_order.append(current)

        # Step 3: Reduce the in-degree of neighbors
        for neighbor in range(max_n):
            if neighbor in edges[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
    
    return topological_order


def take_middle_of_invalid_updates(rules: Rules, updates: Generator[Update, None, None]) -> Generator[int, None, None]:
    '''
    Take the middle page of the invalid updates,
    after making them valid by applying the topological sort
    '''

    for update in updates:
        if not test_valid_update(rules, update):
            valid_update = topological_sort(update, rules, max(update) + 1)
            middle_page = valid_update[len(valid_update)//2]
            yield middle_page


def main():
    rules, updates = read_input()
    invalid_middle_pages = take_middle_of_invalid_updates(rules, updates)
    result = sum(invalid_middle_pages)
    print(result)


if __name__ == '__main__':
    main()
