"""In expected, actual và PASS/FAIL của các ca độc lập tuần 2."""

from __future__ import annotations

from src.core import BoardError, is_complete_solution, solve_sudoku
from src.terminal import EXAMPLES

SOLUTION = ((1, 2, 3, 4), (3, 4, 1, 2), (2, 1, 4, 3), (4, 3, 2, 1))
UNSAT = [[0, 0, 0, 4], [0, 0, 0, 0], [2, 0, 1, 0], [4, 0, 0, 0]]


def with_cells(*cells: tuple[int, int, int]) -> list[list[int]]:
    board = [[0] * 4 for _ in range(4)]
    for row, col, value in cells:
        board[row][col] = value
    return board


CASES = [
    ("VD01", EXAMPLES[1], "đúng nghiệm phiếu", SOLUTION),
    ("VD02", EXAMPLES[2], "đúng nghiệm phiếu", SOLUTION),
    ("PHIEU01", SOLUTION, "giữ nguyên bảng đầy", SOLUTION),
    ("PHIEU03", with_cells((0, 0, 1), (0, 1, 1)), "đề không hợp lệ", None),
    ("PHIEU04", with_cells((0, 0, 5)), "đề không hợp lệ", None),
    ("PHIEU05", [[0] * 4 for _ in range(4)], "một nghiệm hợp lệ", None),
    ("TK01", [list(row) for row in SOLUTION[:-1]] + [[4, 3, 2, 0]], "đúng nghiệm phiếu", SOLUTION),
    ("TK02", UNSAT, "không có nghiệm", None),
    ("BIEN01", with_cells((3, 3, 1)), "một nghiệm hợp lệ", None),
    ("BIEN02", [[0, 2, 3, 4], *[list(row) for row in SOLUTION[1:]]], "đúng nghiệm phiếu", SOLUTION),
    ("BIEN03", [[0, 0, 3, 4], *[list(row) for row in SOLUTION[1:]]], "đúng nghiệm phiếu", SOLUTION),
    ("LOI01", [[0] * 4 for _ in range(3)], "đề không hợp lệ", None),
    ("LOI02", with_cells((0, 0, 1), (2, 0, 1)), "đề không hợp lệ", None),
    ("LOI03", with_cells((0, 0, 1), (1, 1, 1)), "đề không hợp lệ", None),
    ("LOI04", with_cells((0, 0, -1)), "đề không hợp lệ", None),
]


def main() -> int:
    passed = 0
    for code, board, expected, exact in CASES:
        try:
            result = solve_sudoku(board)
            if result.board is None:
                actual = "không có nghiệm"
                okay = expected == actual
            else:
                actual = "một nghiệm hợp lệ" if is_complete_solution(board, result.board) else "nghiệm sai"
                okay = actual == "một nghiệm hợp lệ" and (
                    expected == "một nghiệm hợp lệ" or result.board == exact
                )
                if expected == "đúng nghiệm phiếu" or expected == "giữ nguyên bảng đầy":
                    actual = f"{actual}; đúng bảng kỳ vọng={result.board == exact}"
        except BoardError:
            actual = "đề không hợp lệ"
            okay = expected == actual
        passed += okay
        print(f"{code}: input={board!r}")
        print(f"  expected={expected}; actual={actual}; {'PASS' if okay else 'FAIL'}")
    print(f"TỔNG KẾT: {passed}/{len(CASES)} ca độc lập đạt")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
