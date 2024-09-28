import numpy as np
from typing import Tuple, List
from config import *
import cv2

class Gem:
    def __init__(self, color: GemColor, position: Tuple[int, int]):
        self.color: GemColor = color
        self.position: Tuple[int, int] = position
        self.x: int = position[0]
        self.y: int = position[1]

    def __str__(self) -> str:
        return f'Gem({self.color}, {self.position})'

    def __repr__(self) -> str:
        return f'Gem({self.color}, {self.position})'

    def __eq__(self, other: 'Gem') -> bool:
        return self.color == other.color and self.position == other.position

    def __hash__(self) -> int:
        return hash((self.color, self.position))

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
        """
        Update the board from a screenshot of the board area.
        
        Args:
            board_screenshot (np.ndarray): A numpy array representing the screenshot of the board area.
                                           The color order is expected to be RGB.
        """
        print(f'Updating board from screenshot...')
        board_state = np.empty(self.size, dtype=object)
        gem_width, gem_height = GEM_SIZE
        inner_margin = 0.2  # 20% margin from each side

        for row in range(BOARD_SIZE[0]):
            for col in range(BOARD_SIZE[1]):
                x_start = int(col * gem_width + gem_width * inner_margin)
                x_end = int((col + 1) * gem_width - gem_width * inner_margin)
                y_start = int(row * gem_height + gem_height * inner_margin)
                y_end = int((row + 1) * gem_height - gem_height * inner_margin)

                gem_area = board_screenshot[y_start:y_end, x_start:x_end]
                average_color = np.mean(gem_area, axis=(0, 1))  # RGB order
                average_color = Color(*average_color)

                # Match the average color to a GemColor
                for gem_color in GemColor:
                    color_range = GemColorRanges[gem_color]
                    if color_range.contains(average_color):
                        board_state[row, col] = Gem(gem_color, (row, col))
                        break
                else:
                    print(f"Warning: Unrecognized color {average_color} at position ({row}, {col})")
                    board_state[row, col] = None
                    if DEBUG_MODE:
                        cv2.imshow('unknown', cv2.cvtColor(gem_area, cv2.COLOR_RGB2BGR))
                        cv2.waitKey()

        self.grid = board_state

    def get_gem(self, row: int, col: int) -> Gem:
        """Get the gem at a specific position."""
        return self.grid[row, col]

    def set_gem(self, row: int, col: int, color: GemColor) -> None:
        """Set the gem at a specific position."""
        self.grid[row, col] = Gem(color, (row, col))

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
        rows = []
        for row in self.grid:
            gems = []
            for gem in row:
                if gem:
                    gems.append(f'{str(gem.color):8}')
                else:
                    gems.append('   None  ')
            rows.append('\t'.join(gems))
        return '\n'.join(rows)
