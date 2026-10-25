"""Tạo các đề Sudoku 4×4 ngẫu nhiên từ một đề đã có nghiệm duy nhất.

Hoán vị số, đổi hàng trong cùng dải, đổi cột trong cùng chồng, đổi dải/chồng
và chuyển vị đều bảo toàn quy tắc Sudoku và số lượng nghiệm.
"""

from __future__ import annotations

import random

SEED_PUZZLE: tuple[tuple[int, ...], ...] = (
    (1, 0, 0, 4),
    (0, 0, 1, 0),
    (0, 4, 0, 0),
    (3, 0, 0, 0),
)


def _axis_order(rng: random.Random) -> list[int]:
    groups = [[0, 1], [2, 3]]
    for group in groups:
        rng.shuffle(group)
    rng.shuffle(groups)
    return [index for group in groups for index in group]


def random_puzzle(rng: random.Random | None = None) -> list[list[int]]:
    """Trả một đề 4×4 hợp lệ, có một nghiệm và 11 ô trống."""
    rng = rng or random.SystemRandom()
    digits = [1, 2, 3, 4]
    rng.shuffle(digits)
    mapping = dict(zip(range(1, 5), digits))
    rows, cols = _axis_order(rng), _axis_order(rng)
    transpose = rng.choice((False, True))
    puzzle: list[list[int]] = []
    for row in rows:
        output_row: list[int] = []
        for col in cols:
            value = SEED_PUZZLE[col][row] if transpose else SEED_PUZZLE[row][col]
            output_row.append(mapping[value] if value else 0)
        puzzle.append(output_row)
    return puzzle
