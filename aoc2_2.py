from typing import Generator

INPUT_FILE = 'aoc2_input.txt'  # Solution: 290

Report = list[int]

def test_increasing(report: Report) -> tuple[bool, int|None]:
    for (i, x), y in zip(enumerate(report), report[1:]):
        if x >= y or abs(x - y) > 3:
            return False, i
    return True, None


def test_decreasing(report: Report) -> tuple[bool, int|None]:
    for (i, x), y in zip(enumerate(report), report[1:]):
        if x <= y or abs(x - y) > 3:
            return False, i
    return True, None


def test_incr_or_decr(report: Report) -> tuple[bool, int|None]:
    assert len(report) > 1, 'Not implemented'

    n_0, n_1 = report[:2]
    if n_0 > n_1:
        # All decreasing
        return test_decreasing(report)
    elif n_0 < n_1:
        # All increasing
        return test_increasing(report)

    return False, 0


def test_report(report: Report) -> int:
    assert len(report) > 1
    ok, err_i = test_incr_or_decr(report)
    if ok:
        return 1
    
    # Try removing elements that led to errors,
    #     or the first element directly.
    for i in {err_i, err_i+1, 0}:
        r = report[:i] + report[i+1:]
        ok, _ = test_incr_or_decr(r)
        if ok:
            return 1

    return 0


def parse_reports() -> Generator[Report, None, None]:
    with open(INPUT_FILE) as f:
        for line in f:
            yield [ int(x) for x in line.strip().split() ]


def main():
    tot_count = sum(test_report(report) for report in parse_reports())
    print(tot_count)


if __name__ == '__main__':
    main()

