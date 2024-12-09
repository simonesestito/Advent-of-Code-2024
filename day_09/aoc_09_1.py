import sys
from typing import Generator
from aoc_09_utils import AllocatedFile, read_input, compute_checksum


def iter_left_to_right_blocks(all_allocated_files: list[AllocatedFile], all_free_blocks: list[int]) -> Generator[int|None, None, None]:
    '''
    Iterate over the allocated files and free blocks, in a left-to-right standard order.
    We yield the file_id of the file in each block.
    "None" is the special value for a free block.
    '''
    for (file_id, alloc), free in zip(all_allocated_files, all_free_blocks):
        # Iterate over the allocated file
        for _ in range(alloc):
            yield file_id

        # Iterate the free blocks
        for _ in range(free):
            yield None


def iter_right_to_left_alloc_block(all_allocated_files: list[AllocatedFile]) -> Generator[int, None, None]:
    '''
    Iterate over the allocated files in reverse order, from right to left.
    We yield the file_id of the file in each block.
    We are not interested in the free blocks in this case.
    '''
    for file_id, alloc in reversed(all_allocated_files):
        for _ in range(alloc):
            yield file_id


def compact_blocks(original_allocated_blocks: list[AllocatedFile], free_blocks: list[int]) -> Generator[int, None, None]:
    '''
    Compact the allocated blocks in the disk, moving the files to the leftmost free space.
    We yield the file_id of the file in each block, in a left-to-right standard order.
    '''
    # We need 2 cursors to iterate over the allocated files and the free blocks, in opposite directions
    left_to_right_blocks_cursor = iter_left_to_right_blocks(original_allocated_blocks, free_blocks)
    right_to_left_files_cursor = iter_right_to_left_alloc_block(original_allocated_blocks)

    # Compute the total number of allocated blocks in the disk:
    # this way, we know when to stop the iteration
    total_blocks = sum(alloc for _, alloc in original_allocated_blocks)
    
    for _ in range(total_blocks):
        # Move the last allocated file's block, to the first available free space.

        # Where are we now in the cursor of the entire disk? In a free space or in an allocated file?
        curr_block_file_id = next(left_to_right_blocks_cursor)
        if curr_block_file_id is None:
            # We have encountered a free block, we need to move the next allocated file to this space
            yield next(right_to_left_files_cursor)
        else:
            # We are in an allocated file, we can just yield it
            yield curr_block_file_id


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
