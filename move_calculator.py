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

from typing import List, Tuple
from board import Board, Gem
from copy import deepcopy

class Move:
    def __init__(self, gem1: Gem, gem2: Gem):
        self.gem1 = gem1
        self.gem2 = gem2

    def __str__(self):
        return f"Move({self.gem1}, {self.gem2})"

class BoardSimulator:
    @staticmethod
    def simulate_move(board: Board, move: Move) -> Tuple[Board, int]:
        simulated_board = deepcopy(board)
        score = 0

        # Swap gems
        simulated_board.grid[move.gem1.position], simulated_board.grid[move.gem2.position] = \
            simulated_board.grid[move.gem2.position], simulated_board.grid[move.gem1.position]

        # Check for matches and apply cascading effects
        while True:
            matches = BoardSimulator.find_matches(simulated_board)
            if not matches:
                break

            score += len(matches)
            BoardSimulator.remove_matches(simulated_board, matches)
            BoardSimulator.apply_gravity(simulated_board)

        return simulated_board, score

    @staticmethod
    def find_matches(board: Board) -> List[Gem]:
        matches = []
        for row in range(board.size[0]):
            for col in range(board.size[1]):
                gem = board.get_gem(row, col)
                if gem is None:
                    continue
                horizontal_match = BoardSimulator.check_match(board, gem, (0, 1))
                vertical_match = BoardSimulator.check_match(board, gem, (1, 0))
                matches.extend(horizontal_match + vertical_match)
        return list(set(matches))  # Remove duplicates

    @staticmethod
    def check_match(board: Board, gem: Gem, direction: Tuple[int, int]) -> List[Gem]:
        matches = [gem]
        for step in [1, -1]:
            row, col = gem.position
            while True:
                row += direction[0] * step
                col += direction[1] * step
                if not board.is_valid_position(row, col):
                    break
                next_gem = board.get_gem(row, col)
                if next_gem is None or next_gem.color != gem.color:
                    break
                matches.append(next_gem)
        return matches if len(matches) >= 3 else []

    @staticmethod
    def remove_matches(board: Board, matches: List[Gem]):
        for gem in matches:
            board.grid[gem.position] = None

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
    def evaluate_move(board: Board, move: Move) -> int:
        _, score = BoardSimulator.simulate_move(board, move)
        return score

class MoveCalculator:
    def __init__(self):
        self.board_simulator = BoardSimulator()
        self.move_evaluator = MoveEvaluator()

    def find_best_move(self, board: Board) -> Move:
        best_move = None
        best_score = -1

        for row in range(board.size[0]):
            for col in range(board.size[1]):
                current_gem = board.get_gem(row, col)
                if current_gem is None:
                    continue

                adjacent_positions = board.get_adjacent_positions(row, col)
                for adj_row, adj_col in adjacent_positions:
                    adjacent_gem = board.get_gem(adj_row, adj_col)
                    if adjacent_gem is None:
                        continue

                    move = Move(current_gem, adjacent_gem)
                    score = self.move_evaluator.evaluate_move(board, move)

                    if score > best_score:
                        best_score = score
                        best_move = move

        return best_move
