import numpy as np
from typing import Tuple, List

class Board:
    def __init__(self, size: Tuple[int, int]):
        self.size: Tuple[int, int] = size
        self.grid: np.ndarray = np.zeros(size, dtype=int)

    def update(self, new_state: np.ndarray) -> None:
        """Update the board with a new state."""
        if new_state.shape != self.size:
            raise ValueError("New state size does not match board size")
        self.grid = new_state

    def get_gem(self, row: int, col: int) -> int:
        """Get the gem color at a specific position."""
        return self.grid[row, col]

    def set_gem(self, row: int, col: int, color: int) -> None:
        """Set the gem color at a specific position."""
        self.grid[row, col] = color

    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is valid on the board."""
        return 0 <= row < self.size[0] and 0 <= col < self.size[1]

    def get_adjacent_positions(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get valid adjacent positions for a given position."""
        adjacent = [
            (row-1, col), (row+1, col),
            (row, col-1), (row, col+1)
        ]
        return [(r, c) for r, c in adjacent if self.is_valid_position(r, c)]

    def __str__(self) -> str:
        """String representation of the board."""
        return str(self.grid)

