"""Kiểm chứng dữ liệu nhập web cho cùng lõi đã dùng ở terminal."""

import unittest

from scripts.test_catalog import BACKTRACK, BACKTRACK_SOLUTION, UNSAT
from src.terminal import EXAMPLES
from src.web.model import evaluate, parse_cells


def text_rows(board):
    return [["" if value == 0 else str(value) for value in row] for row in board]


class WebModelTests(unittest.TestCase):
    def test_both_assignment_examples_match_terminal_core(self):
        for index, board in EXAMPLES.items():
            with self.subTest(example=index):
                outcome = evaluate(text_rows(board), solve=True)
                self.assertEqual(outcome.status, "solved")
                self.assertEqual(outcome.result.board[3][3], 1)

    def test_bad_cell_is_reported_at_its_position(self):
        rows = text_rows(EXAMPLES[1])
        rows[2][1] = "5"
        outcome = evaluate(rows, solve=True)
        self.assertEqual(outcome.status, "invalid")
        self.assertIn("(3, 2)", outcome.message)

    def test_check_only_does_not_solve(self):
        outcome = evaluate(text_rows(EXAMPLES[1]), solve=False)
        self.assertEqual(outcome.status, "valid")
        self.assertIsNone(outcome.result)

    def test_valid_unsolvable_board_has_distinct_state(self):
        outcome = evaluate(text_rows(UNSAT), solve=True)
        self.assertEqual(outcome.status, "unsolved")
        self.assertIsNone(outcome.result.board)

    def test_solvable_backtrack_case_matches_independent_expected_board(self):
        outcome = evaluate(text_rows(BACKTRACK), solve=True)
        self.assertEqual(outcome.status, "solved")
        self.assertEqual(outcome.result.board, BACKTRACK_SOLUTION)
        self.assertGreater(outcome.result.backtracks, 0)

    def test_blank_and_zero_mean_same_empty_cell(self):
        empty = [[" "] * 4 for _ in range(4)]
        empty[0][0] = "0"
        self.assertEqual(parse_cells(empty), ((0, 0, 0, 0),) * 4)


if __name__ == "__main__":
    unittest.main()
