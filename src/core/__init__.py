"""Phần lõi dùng chung cho terminal và web."""

from .validation import BoardError, can_place, validate_board

__all__ = ["BoardError", "can_place", "validate_board"]
