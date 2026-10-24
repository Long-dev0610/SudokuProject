"""Giao diện terminal giai đoạn tuần 1."""

from __future__ import annotations

import argparse
import sys

from src.core import BoardError, can_place, validate_board

EXAMPLES = {
    1: [[1, 0, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 0]],
    2: [[0, 2, 3, 4], [3, 4, 1, 2], [2, 1, 0, 3], [4, 3, 2, 1]],
}


def read_board() -> list[list[int]]:
    print("Nhập 4 dòng, mỗi dòng gồm 4 số 0–4 cách nhau bằng khoảng trắng:")
    rows = []
    for index in range(1, 5):
        raw = input(f"Hàng {index}: ")
        try:
            rows.append([int(token) for token in raw.split()])
        except ValueError as exc:
            raise BoardError(f"Hàng {index} phải chỉ chứa số nguyên.") from exc
    return rows


def format_board(board: tuple[tuple[int, ...], ...]) -> str:
    lines = []
    for index, row in enumerate(board):
        if index == 2:
            lines.append("------+------")
        lines.append(f"{row[0]} {row[1]} | {row[2]} {row[3]}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    # Windows PowerShell có thể để stdout ở cp1252 dù nguồn là UTF-8.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="Kiểm tra đề Sudoku 4×4, giai đoạn tuần 1")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--example", type=int, choices=(1, 2), help="Nạp ví dụ từ phiếu")
    source.add_argument("--input", action="store_true", help="Nhập 16 số từ bàn phím")
    parser.add_argument(
        "--check", nargs=3, type=int, metavar=("ROW", "COL", "VALUE"),
        help="Kiểm số cần đặt; ROW và COL tính từ 1",
    )
    args = parser.parse_args(argv)
    try:
        raw = EXAMPLES[args.example] if args.example else read_board()
        board = validate_board(raw)
        print(format_board(board))
        print("ĐỀ HỢP LỆ: kích thước, miền giá trị và các số cho trước không xung đột.")
        if args.check:
            row, col, value = args.check
            possible = can_place(board, row - 1, col - 1, value)
            print(f"Đặt {value} vào ({row}, {col}): {'HỢP LỆ' if possible else 'KHÔNG HỢP LỆ'}")
        print("Bộ giải quay lui sẽ được bổ sung ở tuần 2.")
        return 0
    except (BoardError, ValueError) as exc:
        print(f"ĐỀ KHÔNG HỢP LỆ: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
