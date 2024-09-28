from config import BOARD_REGION, GEM_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from mouse import Mouse
from board import Gem
from move_calculator import Move
import time
from typing import Tuple

class MoveExecutor:
    def __init__(self):
        self.board_left: int = BOARD_REGION[0]
        self.board_top: int = BOARD_REGION[1]
        self.gem_width: int = GEM_SIZE[0]
        self.gem_height: int = GEM_SIZE[1]

    def execute_move(self, move: Move) -> None:
        # Calculate the screen coordinates for both gems
        x1, y1 = self._get_gem_center(move.gem1.position)
        x2, y2 = self._get_gem_center(move.gem2.position)

        Mouse.drag(start_x=x1, start_y=y1, end_x=x2, end_y=y2, duration=0.1)

    def _get_gem_center(self, position: Tuple[int, int]) -> Tuple[int, int]:
        row, col = position
        x = self.board_left + (col + 0.5) * self.gem_width
        y = self.board_top + (row + 0.5) * self.gem_height

        return int(x), int(y)
