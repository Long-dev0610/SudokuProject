"""Phần lõi dùng chung cho terminal và web."""

from .validation import BoardError, can_place, validate_board
from .solver import SolveResult, TraceEvent, is_complete_solution, solve_sudoku

__all__ = [
    "BoardError", "SolveResult", "TraceEvent", "can_place", "is_complete_solution",
    "solve_sudoku", "validate_board",
]
