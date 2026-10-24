"""Chuyển dữ liệu từ lưới web sang lõi và chuẩn bị trạng thái hiển thị."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from src.core import BoardError, SolveResult, solve_sudoku, validate_board

Board = tuple[tuple[int, ...], ...]
Status = Literal["invalid", "valid", "unsolved", "solved"]


@dataclass(frozen=True)
class WebOutcome:
    status: Status
    message: str
    original: Board | None = None
    result: SolveResult | None = None


def parse_cells(rows: Sequence[Sequence[str]]) -> Board:
    """Ô rỗng/0 thành 0; các giá trị khác phải là một chữ số 1–4."""
    if len(rows) != 4:
        raise BoardError("Bảng phải gồm đúng 4 hàng.")
    parsed: list[list[int]] = []
    for row_index, row in enumerate(rows, start=1):
        if len(row) != 4:
            raise BoardError(f"Hàng {row_index} phải gồm đúng 4 ô.")
        parsed_row = []
        for col_index, raw in enumerate(row, start=1):
            value = raw.strip() if isinstance(raw, str) else None
            if value in ("", "0"):
                parsed_row.append(0)
            elif value in ("1", "2", "3", "4"):
                parsed_row.append(int(value))
            else:
                raise BoardError(f"Ô ({row_index}, {col_index}) chỉ nhận số 1–4 hoặc để trống.")
        parsed.append(parsed_row)
    return validate_board(parsed)


def evaluate(rows: Sequence[Sequence[str]], *, solve: bool) -> WebOutcome:
    """Phân biệt đề sai, hợp lệ, vô nghiệm và có nghiệm bằng cùng lõi terminal."""
    try:
        original = parse_cells(rows)
    except BoardError as exc:
        return WebOutcome("invalid", str(exc))
    if not solve:
        return WebOutcome("valid", "Đề hợp lệ. Có thể bắt đầu giải.", original)
    result = solve_sudoku(original, record_trace=True)
    if result.board is None:
        return WebOutcome("unsolved", "Đề hợp lệ nhưng không có nghiệm.", original, result)
    return WebOutcome("solved", "Đã tìm được một nghiệm hợp lệ.", original, result)
