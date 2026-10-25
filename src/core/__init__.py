"""Phần lõi dùng chung cho terminal và web."""

from .validation import BoardError, can_place, placement_conflicts, validate_board
from .solver import SolveResult, TraceEvent, is_complete_solution, solve_sudoku

__all__ = [
    "BoardError", "SolveResult", "TraceEvent", "can_place", "placement_conflicts", "is_complete_solution",
    "solve_sudoku", "validate_board",
]
