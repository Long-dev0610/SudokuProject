"""Oracle độc lập: liệt kê mọi bảng Sudoku 4×4 đầy hợp lệ bằng hoán vị."""

from itertools import permutations
import sys

from src.terminal import EXAMPLES

UNSAT = ((0, 0, 0, 4), (0, 0, 0, 0), (2, 0, 1, 0), (4, 0, 0, 0))
BACKTRACK = ((1, 0, 0, 4), (0, 0, 1, 0), (0, 4, 0, 0), (3, 0, 0, 0))


def all_solutions():
    rows = tuple(permutations((1, 2, 3, 4)))
    for top_left in rows:
        for top_right in rows:
            if set(top_left[:2]) & set(top_right[:2]):
                continue
            if set(top_left[2:]) & set(top_right[2:]):
                continue
            for bottom_left in rows:
                if any(len({top_left[c], top_right[c], bottom_left[c]}) < 3 for c in range(4)):
                    continue
                for bottom_right in rows:
                    board = (top_left, top_right, bottom_left, bottom_right)
                    if all(len({row[c] for row in board}) == 4 for c in range(4)) and all(
                        len({board[r][c] for r in range(r0, r0 + 2) for c in range(c0, c0 + 2)}) == 4
                        for r0 in (0, 2) for c0 in (0, 2)
                    ):
                        yield board


def matching(solutions, given):
    return [
        board for board in solutions
        if all(given[r][c] == 0 or given[r][c] == board[r][c] for r in range(4) for c in range(4))
    ]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    solutions = list(all_solutions())
    counts = {
        "tổng bảng hợp lệ": len(solutions),
        "ví dụ 1": len(matching(solutions, EXAMPLES[1])),
        "ví dụ 2": len(matching(solutions, EXAMPLES[2])),
        "đề vô nghiệm TK02": len(matching(solutions, UNSAT)),
        "đề quay lui TK03": len(matching(solutions, BACKTRACK)),
    }
    for label, count in counts.items():
        print(f"{label}: {count}")
    if counts != {"tổng bảng hợp lệ": 288, "ví dụ 1": 1, "ví dụ 2": 1, "đề vô nghiệm TK02": 0, "đề quay lui TK03": 1}:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
