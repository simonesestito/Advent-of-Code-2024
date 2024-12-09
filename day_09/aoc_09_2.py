import sys
from typing import Generator
from collections import defaultdict
from aoc_09_utils import AllocatedFile, read_input, compute_checksum
from aoc_09_1 import iter_left_to_right_blocks


def compact_blocks(original_allocated_blocks: list[AllocatedFile], free_blocks: list[int]) -> Generator[int|None, None, None]:
    '''
    Compact the allocated blocks in the disk, moving the files to the leftmost free space.
    We yield the file_id of the file in each block, in a left-to-right standard order.
    '''
    # Keep track of where a file has been moved
    # moved_files[file_id] = index_of_free_space_where_it_was_moved
    moved_files: dict[int, int] = {}

    # Keep track of the files moved in each free block
    # moved_in_free_block[index_of_free_space_where_it_was_moved] = list[file_id]
    moved_in_free_block: dict[int, list[int]] = defaultdict(list)

    # Start the moving process from the rightmost file
    for i, (file_id, alloc_space) in reversed(list(enumerate(original_allocated_blocks))):
        # Is there a free space to move the file?
        # We can only accept to move it to free spaces that are at the left of the file
        for j, free_space in enumerate(free_blocks[:i]):
            if free_space >= alloc_space:
                # Move the file to the leftmost free space
                free_blocks[j] -= alloc_space
                moved_files[file_id] = j
                moved_in_free_block[j].append(file_id)
                break

    # Given the moved_files structure we just built, we can now iterate over the compacted blocks and reconstruct the disk
    for i, (file_id, alloc_space) in enumerate(original_allocated_blocks):
        # Print the current file
        if file_id not in moved_files:
            # This file is still where it was originally (= here)
            yield from (file_id for _ in range(alloc_space))
        else:
            # It WAS moved!
            # A file can only be moved to the left, and we are iterating from left to right,
            # so it is safe to assume that this space is now free
            yield from (None for _ in range(alloc_space))

        # Now, think about the corresponding free space that appears after this file
        free_space = free_blocks[i]
        blocks_moved_here = moved_in_free_block[i]
        for moved_file in blocks_moved_here:
            # Print the file that was moved here
            moved_file_space = original_allocated_blocks[moved_file][1]
            yield from (moved_file for _ in range(moved_file_space))

        # Print the remaining free space.
        # It has already been decreased during the file moving process
        yield from (None for _ in range(free_space))


def show_example():
    original_allocated_blocks, free_blocks = read_input('aoc_09_example.txt')

    # Visualize the parsed input
    print('Parsed input:', file=sys.stderr)
    for file_id in iter_left_to_right_blocks(original_allocated_blocks, free_blocks):
        # Print the allocated file, or free block if file_id is None
        print('.' if file_id is None else file_id, end='', file=sys.stderr)
    print('\n', file=sys.stderr)

    compacted_blocks = compact_blocks(original_allocated_blocks, free_blocks)
    compacted_blocks = list(compacted_blocks)  # Only with the example input, we can afford to do this

    # Visualize the compacted blocks
    print('Compacted blocks:', file=sys.stderr)
    for file_id in compacted_blocks:
        # Print the allocated file, or free block if file_id is None
        print('.' if file_id is None else file_id, end='', file=sys.stderr)
    print('\n', file=sys.stderr)

    result = compute_checksum(compacted_blocks)
    print(f'Checksum: {result}\n\n', file=sys.stderr)


def main():
    original_allocated_blocks, free_blocks = read_input()
    compacted_blocks = compact_blocks(original_allocated_blocks, free_blocks)
    result = compute_checksum(compacted_blocks)
    print(result)


if __name__ == '__main__':
    show_example()  # Show the process with the example input
    main()
