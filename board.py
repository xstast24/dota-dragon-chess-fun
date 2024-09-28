import numpy as np
from typing import Tuple, List
from config import *
import cv2


class Board:
    def __init__(self, size: Tuple[int, int]):
        self.size: Tuple[int, int] = size
        self.grid: np.ndarray = np.empty(size, dtype=object)

    def update(self, new_state: np.ndarray) -> None:
        """Update the board with a new state."""
        if new_state.shape != self.size:
            raise ValueError("New state size does not match board size")
        self.grid = new_state

    def update_from_screenshot(self, board_screenshot: np.ndarray) -> None:
        """Update the board from a screenshot of the board area."""
        board_state = np.empty(self.size, dtype=object)
        gem_width, gem_height = GEM_SIZE
        inner_margin = 0.2  # 20% margin from each side

        for row in range(BOARD_SIZE[0]):
            for col in range(BOARD_SIZE[1]):
                print(f'Row: {row}, Col: {col}')
                x_start = int(col * gem_width + gem_width * inner_margin)
                x_end = int((col + 1) * gem_width - gem_width * inner_margin)
                y_start = int(row * gem_height + gem_height * inner_margin)
                y_end = int((row + 1) * gem_height - gem_height * inner_margin)

                gem_area = board_screenshot[y_start:y_end, x_start:x_end]
                average_color = np.mean(gem_area, axis=(0, 1))  # BGR order
                average_color_rgb = Color(*average_color[::-1])  # Convert BGR to RGB

                # Match the average color to a GemColor
                for gem_color in GemColor:
                    color_range = GemColorRanges[gem_color]
                    if color_range.contains(average_color_rgb):
                        board_state[row, col] = gem_color
                        break
                else:
                    print(f"Warning: Unrecognized color {average_color_rgb} at position ({row}, {col})")
                    board_state[row, col] = None
                    if DEBUG_MODE:
                        cv2.imshow('unknown', gem_area)
                        cv2.waitKey()

        self.grid = board_state

    def get_gem(self, row: int, col: int) -> GemColor:
        """Get the gem color at a specific position."""
        return self.grid[row, col]

    def set_gem(self, row: int, col: int, color: GemColor) -> None:
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
