"""
Move Detector Module

This module implements the game logic for detecting and evaluating moves in a gem-matching game.
The architecture consists of the following components:

1. MoveDetector: Main class responsible for finding the best move.
2. Move: A class representing a single move (gem swap).
3. MoveEvaluator: A class for evaluating the outcome and score of a move.
4. BoardSimulator: A class for simulating moves on a copy of the board.

The process of finding the best move involves:
1. Generating all possible moves.
2. Simulating each move and its cascading effects.
3. Evaluating the score for each move.
4. Selecting the move with the highest score.

This design allows for easy extension and modification of the scoring system
and move evaluation logic.
"""

from copy import deepcopy
from typing import List, Optional, Tuple, Iterable

from board import Board, Gem
from config import GemColor


class Move:
    def __init__(self, gem1: Gem, gem2: Gem):
        self.gem1 = gem1
        self.gem2 = gem2
        self.sequences: dict[GemColor, int] = {}

    @property
    def cleared_gems(self) -> int:
        return sum(self.sequences.values())

    @property
    def longest_sequence(self) -> int:
        return max(self.sequences.values())

    def __str__(self):
        return f"Move({self.gem1}, {self.gem2}, {self.sequences})"


class BoardSimulator:
    def __init__(self, board: Board) -> None:
        self.orig_board = board
        self.board = deepcopy(board)

    def simulate_move(self, move: Move) -> None:
        # Swap gems
        self.board.set_gem(*move.gem1.position, move.gem2.color)
        self.board.set_gem(*move.gem2.position, move.gem1.color)

        # Get new gems (after the swap)
        gem1 = self.board.get_gem(*move.gem1.position)
        gem2 = self.board.get_gem(*move.gem2.position)

        # TODO for simplicity, let's start with counting only the direct matches of the move, later use the repeating calculation below
        for gem in [gem1, gem2]:
            matches = self.get_valid_matches(gem)
            move.sequences[gem.color] = len(matches)

        # TODO calculate matches, clear gems, apply gravity, calculate new matches, repeat...
        # Check for matches and apply cascading effects
        # while True:
        #     matches = BoardSimulator.find_all_matches(simulated_board)
        #     if not matches:
        #         break

        #     score += len(matches)
        #     BoardSimulator.remove_matches(simulated_board, matches)
        #     BoardSimulator.apply_gravity(simulated_board)

    def get_valid_matches(self, gem: Gem) -> List[Gem]:
        """Get matching gems connected to this gem, including this gem. Only if there is a valid match of 3 or more gems, otherwise empty list."""
        horizontal = self.check_directional_matches(gem, direction=(0, 1))
        vertical = self.check_directional_matches(gem, direction=(1, 0))
        if len(horizontal) >= 3 and len(vertical) >= 3:
            return list(set(horizontal + vertical))
        elif len(horizontal) >= 3:
            return horizontal
        elif len(vertical) >= 3:
            return vertical
        else:
            return []

    def check_directional_matches(self, gem: Gem, direction: Tuple[int, int]) -> List[Gem]:
        """Get matches in a direction, including the original gem. E.g. [1, 0] means vertical, [0, 1] is horizontal, [1, 1] is diagonal"""
        matches = [gem]
        for step in [1, -1]:
            row, col = gem.position
            while True:
                row += direction[0] * step
                col += direction[1] * step
                if not self.board.is_valid_position(row, col):
                    break
                next_gem = self.board.get_gem(row, col)
                if next_gem is None or next_gem.color != gem.color:
                    break
                matches.append(next_gem)
        return matches

    # FIXME old LLM implementation - use self.board and check validity
    @staticmethod
    def find_all_matches(board: Board) -> List[Gem]:
        matches = []
        for row in range(board.size[0]):
            for col in range(board.size[1]):
                gem = board.get_gem(row, col)
                if gem is None:
                    continue
                horizontal_match = BoardSimulator.check_directional_matches(board, gem, (0, 1))
                vertical_match = BoardSimulator.check_directional_matches(board, gem, (1, 0))
                matches.extend(horizontal_match + vertical_match)
        return list(set(matches))  # Remove duplicates

    # FIXME old LLM implementation - use self.board and check validity
    @staticmethod
    def remove_matches(board: Board, matches: List[Gem]):
        for gem in matches:
            board.grid[gem.position] = None

    # FIXME old LLM implementation - use self.board and check validity
    @staticmethod
    def apply_gravity(board: Board):
        for col in range(board.size[1]):
            empty_row = board.size[0] - 1
            for row in range(board.size[0] - 1, -1, -1):
                if board.get_gem(row, col) is not None:
                    board.grid[empty_row, col] = board.get_gem(row, col)
                    board.grid[empty_row, col].position = (empty_row, col)
                    empty_row -= 1
            for row in range(empty_row, -1, -1):
                board.grid[row, col] = None


class MoveEvaluator:
    @staticmethod
    def evaluate_move(board: Board, move: Move) -> None:
        BoardSimulator(board=board).simulate_move(move)


class MoveCalculator:
    def __init__(self):
        self.move_evaluator = MoveEvaluator()

    @staticmethod
    def _get_longest_from(moves: List[Move]) -> Optional[Move]:
        longest = None
        if len(moves) >= 1:
            longest = moves[0]
        for move in moves:
            if move.longest_sequence > longest.longest_sequence:
                longest = move

        return longest

    def calculate_all_valid_moves(self, board: Board) -> List[Move]:
        moves = []
        for row in range(board.size[0]):
            for col in range(board.size[1]):
                current_gem = board.get_gem(row, col)
                if current_gem is None:
                    continue

                adjacent_positions = board.get_adjacent_positions(row, col)
                for adj_row, adj_col in adjacent_positions:
                    adjacent_gem: Gem | None = board.get_gem(adj_row, adj_col)
                    # FIXME use unknown gem instead of None, so it can be calculate dproperly in the simulator (with position etc.)
                    if adjacent_gem is None:
                        continue
                    move = Move(current_gem, adjacent_gem)
                    self.move_evaluator.evaluate_move(board, move)
                    moves.append(move)

        return moves

    def get_all_moves_grouped_by_color(self, board: Board) -> dict[GemColor, list[Move]]:
        all_moves = self.calculate_all_valid_moves(board)
        moves = {}
        for move in all_moves:
            for color in move.sequences.keys():
                try:
                    moves[color].append(move)
                except KeyError:
                    moves[color] = [move]
        return moves

    def find_longest_sequence_move(self, board: Board) -> Optional[Move]:
        moves = self.calculate_all_valid_moves(board)
        return self._get_longest_from(moves)

    def get_move_by_color_ordering(self, board: Board, colors: Iterable[GemColor] = tuple(c for c in GemColor)) -> Optional[Move]:
        """
        Get moves of color 1, if not available, then of color 2, etc. The selected move is the longest available in the first available color.
        Note: There can be longer moves available in other colors, but we ignore them. We want to first deplete one color, then another, etc.
        """
        all_moves = self.get_all_moves_grouped_by_color(board)
        moves = []
        for color in colors:
            try:
                moves = all_moves[color]
                break
            except KeyError:
                continue

        return self._get_longest_from(moves)

    def find_longest_with_color_order(self, board: Board) -> Optional[Move]:
        pass  # TODO rename and implement - should get the longest available, but if multiple colors have the same length, then prioritize by color

    def find_best_move(self, board: Board) -> Optional[Move]:
        raise NotImplementedError()  # TODO
