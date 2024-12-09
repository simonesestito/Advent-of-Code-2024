from typing import NamedTuple, Iterator


class AllocatedFile(NamedTuple):
    file_id: int
    allocated_space: int


def read_input(filename: str = 'aoc_09.txt') -> tuple[list[AllocatedFile], list[int]]:
    '''
    Read the input digits of the file in an organized way.
    They are parsed as file_id, allocated space and the free space afterwards.

    Returns:
    tuple with list of AllocatedFile and the list of free blocks
    Both are in forward order, as they appear in the input file
    '''
    with open(filename) as f:
        raw_line = f.read().strip()

    # Make the whole string as a list[int], parsing digits
    digits_line = [ int(digit) for digit in raw_line ]

    # Since the line may have an odd number of digits,
    # we want to pad it to have always an even number.
    # In this case, it is safe to assume that it has a final 0 blocks free space
    if len(digits_line) % 2 == 1:
        digits_line.append(0)

    all_allocated_blocks = digits_line[::2]  # Even indexes are the allocated space
    all_file_ids = range(len(all_allocated_blocks))

    # Parse them in a more organized structure
    all_allocated_files: list[AllocatedFile] = []
    for file_id, allocated_space in zip(all_file_ids, all_allocated_blocks):
        all_allocated_files.append(AllocatedFile(file_id, allocated_space))

    all_free_blocks: list[int] = digits_line[1::2]  # Odd indexes are the free space afterwards

    return all_allocated_files, all_free_blocks


def compute_checksum(compacted_blocks: Iterator[int]) -> int:
    checksum = 0
    for block_id, file_id in enumerate(compacted_blocks):
        if file_id is not None:
            checksum += block_id * file_id
    return checksum
