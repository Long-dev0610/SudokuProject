"""Kiểm tra đề ngẫu nhiên vẫn đúng luật và giữ nghiệm duy nhất."""

import random
import unittest

from src.core import can_place, validate_board
from src.web.puzzles import random_puzzle


def count_solutions(board: list[list[int]], limit: int = 2) -> int:
    """Bộ đếm độc lập chỉ dùng trong kiểm thử để phát hiện đề nhiều nghiệm."""
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:
                count = 0
                for value in range(1, 5):
                    if can_place(board, row, col, value):
                        board[row][col] = value
                        count += count_solutions(board, limit - count)
                        board[row][col] = 0
                        if count >= limit:
                            return count
                return count
    return 1


class RandomPuzzleTests(unittest.TestCase):
    def test_generated_boards_are_valid_unique_and_varied(self):
        seen = set()
        for seed in range(32):
            board = random_puzzle(random.Random(seed))
            validate_board(board)
            self.assertEqual(sum(value == 0 for row in board for value in row), 11)
            self.assertEqual(count_solutions(board), 1)
            seen.add(tuple(tuple(row) for row in board))
        self.assertGreater(len(seen), 24)


if __name__ == "__main__":
    unittest.main()
