"""Giải Sudoku 4×4 bằng quay lui theo thứ tự hàng rồi cột."""

from __future__ import annotations

from dataclasses import dataclass

from .validation import SIZE, placement_conflicts, validate_board

Board = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class TraceEvent:
    action: str  # "chọn", "thử", "đặt" hoặc "hoàn tác"
    row: int  # 0-based
    col: int  # 0-based
    value: int
    conflicts: tuple[str, ...] = ()  # ràng buộc của lần thử bị vi phạm


@dataclass(frozen=True)
class SolveResult:
    board: Board | None
    attempts: int  # số ứng viên 1..4 đã thử
    placements: int  # số lần gán hợp lệ vào ô trống
    backtracks: int  # số lần hoàn tác về 0
    trace: tuple[TraceEvent, ...] = ()


def is_complete_solution(givens: object, candidate: object) -> bool:
    """Kiểm bảng đầy, đúng Sudoku và giữ nguyên mọi số cho trước."""
    original = validate_board(givens)
    try:
        solved = validate_board(candidate)
    except ValueError:
        return False
    return all(
        solved[row][col] != 0
        and (original[row][col] == 0 or solved[row][col] == original[row][col])
        for row in range(SIZE)
        for col in range(SIZE)
    )


def solve_sudoku(board: object, *, record_trace: bool = False) -> SolveResult:
    """Trả một nghiệm hoặc None; đề sai phát sinh BoardError; không sửa input."""
    original = validate_board(board)
    working = [list(row) for row in original]
    attempts = placements = backtracks = 0
    events: list[TraceEvent] = []

    def search() -> bool:
        nonlocal attempts, placements, backtracks
        empty = next(
            ((row, col) for row in range(SIZE) for col in range(SIZE) if working[row][col] == 0),
            None,
        )
        if empty is None:
            return is_complete_solution(original, working)

        row, col = empty
        if record_trace:
            events.append(TraceEvent("chọn", row, col, 0))
        for value in range(1, SIZE + 1):
            attempts += 1
            conflicts = placement_conflicts(working, row, col, value)
            if record_trace:
                events.append(TraceEvent("thử", row, col, value, conflicts))
            if conflicts:
                continue
            working[row][col] = value
            placements += 1
            if record_trace:
                events.append(TraceEvent("đặt", row, col, value))
            if search():
                return True
            working[row][col] = 0
            backtracks += 1
            if record_trace:
                events.append(TraceEvent("hoàn tác", row, col, value))
        return False

    found = search()
    solved = tuple(tuple(row) for row in working) if found else None
    return SolveResult(solved, attempts, placements, backtracks, tuple(events))
