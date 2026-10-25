"""Kiểm chứng dữ liệu nhập web cho cùng lõi đã dùng ở terminal."""

import unittest

from scripts.test_catalog import BACKTRACK, BACKTRACK_SOLUTION, UNSAT
from src.terminal import EXAMPLES
from src.web.model import evaluate, frame_at, parse_cells


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

    def test_backtracking_replay_preserves_givens_and_ends_at_real_solution(self):
        outcome = evaluate(text_rows(BACKTRACK), solve=True)
        self.assertEqual(frame_at(outcome, 0).board, outcome.original)
        saw_undo = False
        for step in range(1, len(outcome.result.trace) + 1):
            frame = frame_at(outcome, step)
            self.assertTrue(all(
                outcome.original[r][c] == 0 or frame.board[r][c] == outcome.original[r][c]
                for r in range(4) for c in range(4)
            ))
            if frame.event.action == "hoàn tác":
                saw_undo = True
                self.assertEqual(frame.board[frame.event.row][frame.event.col], 0)
        final = frame_at(outcome, len(outcome.result.trace))
        self.assertTrue(saw_undo)
        self.assertEqual(final.board, outcome.result.board)
        self.assertEqual((final.attempts, final.placements, final.backtracks), (55, 18, 7))

    def test_unsolved_replay_restores_original_board(self):
        outcome = evaluate(text_rows(UNSAT), solve=True)
        final = frame_at(outcome, len(outcome.result.trace))
        self.assertEqual(final.board, outcome.original)
        self.assertGreater(final.backtracks, 0)

    def test_full_board_has_zero_step_replay(self):
        solution = [[1, 2, 3, 4], [3, 4, 1, 2], [2, 1, 4, 3], [4, 3, 2, 1]]
        outcome = evaluate(text_rows(solution), solve=True)
        self.assertEqual(len(outcome.result.trace), 0)
        self.assertEqual(frame_at(outcome, 0).board, outcome.result.board)


if __name__ == "__main__":
    unittest.main()
