import unittest

from src.core import BoardError, can_place, validate_board
from src.terminal import EXAMPLES, main


class ValidationTests(unittest.TestCase):
    def test_both_assigned_examples_are_valid(self):
        for example in EXAMPLES.values():
            with self.subTest(example=example):
                self.assertEqual(len(validate_board(example)), 4)

    def test_wrong_shape_is_rejected(self):
        with self.assertRaises(BoardError):
            validate_board([[0] * 4] * 3)
        with self.assertRaises(BoardError):
            validate_board([[0] * 4, [0] * 4, [0] * 4, [0] * 3])

    def test_invalid_cell_values_are_rejected(self):
        for value in (-1, 5, True, 1.5):
            board = [[0] * 4 for _ in range(4)]
            board[0][0] = value
            with self.subTest(value=value), self.assertRaises(BoardError):
                validate_board(board)

    def test_row_column_and_block_conflicts_are_independent(self):
        for pos in ((0, 2), (2, 0), (1, 1)):
            board = [[0] * 4 for _ in range(4)]
            board[0][0] = board[pos[0]][pos[1]] = 1
            with self.subTest(pos=pos), self.assertRaises(BoardError):
                validate_board(board)

    def test_can_place_checks_all_rules_without_mutating(self):
        board = [row.copy() for row in EXAMPLES[1]]
        original = [row.copy() for row in board]
        self.assertTrue(can_place(board, 0, 1, 2))
        self.assertFalse(can_place(board, 0, 1, 1))
        self.assertFalse(can_place(board, 0, 0, 2))
        self.assertEqual(board, original)

    def test_can_place_rejects_bad_arguments(self):
        with self.assertRaises(ValueError):
            can_place(EXAMPLES[1], 4, 0, 2)
        with self.assertRaises(ValueError):
            can_place(EXAMPLES[1], 0, 1, 0)

    def test_cli_examples_run(self):
        self.assertEqual(main(["--example", "1", "--check", "1", "2", "2"]), 0)
        self.assertEqual(main(["--example", "2"]), 0)


if __name__ == "__main__":
    unittest.main()
