"""Các ca kiểm độc lập cho bộ giải và giao diện tuần 2."""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src.core import BoardError, is_complete_solution, placement_conflicts, solve_sudoku, validate_board
from src.terminal import EXAMPLES, main

SOLUTION = ((1, 2, 3, 4), (3, 4, 1, 2), (2, 1, 4, 3), (4, 3, 2, 1))
UNSAT = [[0, 0, 0, 4], [0, 0, 0, 0], [2, 0, 1, 0], [4, 0, 0, 0]]
BACKTRACK = [[1, 0, 0, 4], [0, 0, 1, 0], [0, 4, 0, 0], [3, 0, 0, 0]]
BACKTRACK_SOLUTION = ((1, 3, 2, 4), (4, 2, 1, 3), (2, 4, 3, 1), (3, 1, 4, 2))


class SolverTests(unittest.TestCase):
    def test_example_1_matches_assignment(self):
        self.assertEqual(solve_sudoku(EXAMPLES[1]).board, SOLUTION)

    def test_example_2_matches_assignment(self):
        self.assertEqual(solve_sudoku(EXAMPLES[2]).board, SOLUTION)

    def test_full_valid_board_returns_unchanged(self):
        result = solve_sudoku(SOLUTION)
        self.assertEqual(result.board, SOLUTION)
        self.assertEqual(result.placements, 0)

    def test_empty_board_has_a_valid_solution(self):
        empty = [[0] * 4 for _ in range(4)]
        result = solve_sudoku(empty)
        self.assertIsNotNone(result.board)
        self.assertTrue(is_complete_solution(empty, result.board))

    def test_single_missing_cell_is_filled(self):
        board = [list(row) for row in SOLUTION]
        board[3][3] = 0
        self.assertEqual(solve_sudoku(board).board, SOLUTION)

    def test_duplicate_given_in_row_is_invalid(self):
        board = [list(row) for row in SOLUTION]
        board[0][1] = 1
        with self.assertRaises(BoardError):
            solve_sudoku(board)

    def test_value_five_is_invalid(self):
        board = [list(row) for row in SOLUTION]
        board[0][0] = 5
        with self.assertRaises(BoardError):
            solve_sudoku(board)

    def test_valid_but_unsolvable_board_returns_none(self):
        validate_board(UNSAT)
        result = solve_sudoku(UNSAT)
        self.assertIsNone(result.board)
        self.assertGreater(result.backtracks, 0)

    def test_solvable_board_really_requires_backtracking(self):
        result = solve_sudoku(BACKTRACK, record_trace=True)
        self.assertEqual(result.board, BACKTRACK_SOLUTION)
        self.assertEqual((result.attempts, result.placements, result.backtracks), (55, 18, 7))
        self.assertTrue(any(event.action == "hoàn tác" for event in result.trace))

    def test_solver_does_not_mutate_input(self):
        board = [row.copy() for row in EXAMPLES[1]]
        before = [row.copy() for row in board]
        solve_sudoku(board)
        self.assertEqual(board, before)

    def test_trace_records_placements_and_undo(self):
        result = solve_sudoku(UNSAT, record_trace=True)
        self.assertEqual(sum(e.action == "đặt" for e in result.trace), result.placements)
        self.assertEqual(sum(e.action == "hoàn tác" for e in result.trace), result.backtracks)

    def test_trace_explains_each_attempt_using_real_constraints(self):
        result = solve_sudoku(BACKTRACK, record_trace=True)
        attempts = [event for event in result.trace if event.action == "thử"]
        self.assertEqual(len(attempts), result.attempts)
        self.assertTrue(any(event.conflicts for event in attempts))
        self.assertTrue(any(event.action == "chọn" for event in result.trace))
        self.assertEqual(placement_conflicts(EXAMPLES[1], 0, 1, 1), ("row", "column", "block"))

    def test_solution_checker_rejects_unfilled_board(self):
        self.assertFalse(is_complete_solution(EXAMPLES[1], EXAMPLES[1]))

    def test_solution_checker_rejects_changed_given(self):
        original = [[0] * 4 for _ in range(4)]
        original[0][0] = 2
        self.assertFalse(is_complete_solution(original, SOLUTION))

    def test_terminal_example_prints_solution(self):
        output = io.StringIO()
        with redirect_stdout(output):
            status = main(["--example", "1"])
        self.assertEqual(status, 0)
        self.assertIn("NGHIỆM:", output.getvalue())

    def test_terminal_input_rejects_conflicting_givens(self):
        output = io.StringIO()
        rows = ["1 1 0 0", "0 0 0 0", "0 0 0 0", "0 0 0 0"]
        with patch("builtins.input", side_effect=rows), redirect_stdout(output):
            status = main(["--input"])
        self.assertEqual(status, 2)
        self.assertIn("ĐỀ KHÔNG HỢP LỆ", output.getvalue())

    def test_terminal_input_reports_no_solution(self):
        output = io.StringIO()
        rows = [" ".join(map(str, row)) for row in UNSAT]
        with patch("builtins.input", side_effect=rows), redirect_stdout(output):
            status = main(["--input"])
        self.assertEqual(status, 1)
        self.assertIn("KHÔNG CÓ NGHIỆM", output.getvalue())


if __name__ == "__main__":
    unittest.main()
