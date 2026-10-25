"""Kiểm tra dữ liệu đầu vào của Sudoku 4×4 theo phiếu DT041."""

from __future__ import annotations

from collections.abc import Sequence

SIZE = 4
BLOCK = 2


class BoardError(ValueError):
    """Đề Sudoku sai cấu trúc, miền giá trị hoặc ràng buộc."""


def _normalise_board(board: object) -> tuple[tuple[int, ...], ...]:
    if not isinstance(board, Sequence) or isinstance(board, (str, bytes)):
        raise BoardError("Bảng phải gồm đúng 4 hàng.")
    if len(board) != SIZE:
        raise BoardError("Bảng phải gồm đúng 4 hàng.")
    result: list[tuple[int, ...]] = []
    for row_number, row in enumerate(board, start=1):
        if not isinstance(row, Sequence) or isinstance(row, (str, bytes)) or len(row) != SIZE:
            raise BoardError(f"Hàng {row_number} phải gồm đúng 4 ô.")
        normalised: list[int] = []
        for col_number, value in enumerate(row, start=1):
            if type(value) is not int or not 0 <= value <= SIZE:
                raise BoardError(
                    f"Ô ({row_number}, {col_number}) phải là số nguyên từ 0 đến 4."
                )
            normalised.append(value)
        result.append(tuple(normalised))
    return tuple(result)


def _check_unique(values: Sequence[int], label: str) -> None:
    given = [value for value in values if value != 0]
    if len(given) != len(set(given)):
        raise BoardError(f"Các số cho trước bị trùng trong {label}.")


def validate_board(board: object) -> tuple[tuple[int, ...], ...]:
    """Trả bản bất biến của bảng hợp lệ; ném BoardError nếu đề sai."""
    b = _normalise_board(board)
    for row in range(SIZE):
        _check_unique(b[row], f"hàng {row + 1}")
    for col in range(SIZE):
        _check_unique([b[row][col] for row in range(SIZE)], f"cột {col + 1}")
    for row0 in range(0, SIZE, BLOCK):
        for col0 in range(0, SIZE, BLOCK):
            values = [
                b[row][col]
                for row in range(row0, row0 + BLOCK)
                for col in range(col0, col0 + BLOCK)
            ]
            _check_unique(values, f"khối ({row0 // BLOCK + 1}, {col0 // BLOCK + 1})")
    return b


def placement_conflicts(board: object, row: int, col: int, value: int) -> tuple[str, ...]:
    """Nêu các ràng buộc bị vi phạm mà không sửa bảng."""
    b = validate_board(board)
    if type(row) is not int or type(col) is not int or not (0 <= row < SIZE and 0 <= col < SIZE):
        raise ValueError("Chỉ số hàng và cột phải từ 0 đến 3.")
    if type(value) is not int or not 1 <= value <= SIZE:
        raise ValueError("Giá trị cần đặt phải là số nguyên từ 1 đến 4.")
    if b[row][col] != 0:
        return ("occupied",)
    conflicts = []
    if value in b[row]:
        conflicts.append("row")
    if any(b[r][col] == value for r in range(SIZE)):
        conflicts.append("column")
    row0 = (row // BLOCK) * BLOCK
    col0 = (col // BLOCK) * BLOCK
    if any(
        b[r][c] == value
        for r in range(row0, row0 + BLOCK)
        for c in range(col0, col0 + BLOCK)
    ):
        conflicts.append("block")
    return tuple(conflicts)


def can_place(board: object, row: int, col: int, value: int) -> bool:
    """Kiểm một nước đặt; chỉ số row/col từ 0 đến 3, không sửa bảng."""
    return not placement_conflicts(board, row, col, value)
