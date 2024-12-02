from typing import Generator

INPUT_FILE = 'aoc2_input.txt'  # Solution: 218

Report = list[int]

def test_increasing(report: Report) -> bool:
    for x, y in zip(report, report[1:]):
        if x >= y or abs(x - y) > 3:
            return False
    return True


def test_decreasing(report: Report) -> bool:
    for x, y in zip(report, report[1:]):
        if x <= y or abs(x - y) > 3:
            return False
    return True


def test_incr_or_decr(report: Report) -> bool:
    assert len(report) > 1, 'Not implemented'

    n_0, n_1 = report[:2]
    if n_0 > n_1:
        # All decreasing
        return test_decreasing(report)
    elif n_0 < n_1:
        # All increasing
        return test_increasing(report)

    return False  # The first two elements are equal


def test_report(report: Report) -> int:
    assert len(report) > 1
    return 1 if test_incr_or_decr(report) else 0


def parse_reports() -> Generator[Report, None, None]:
    with open(INPUT_FILE) as f:
        for line in f:
            yield [ int(x) for x in line.strip().split() ]


def main():
    tot_count = sum(test_report(report) for report in parse_reports())
    print(tot_count)


if __name__ == '__main__':
    main()

