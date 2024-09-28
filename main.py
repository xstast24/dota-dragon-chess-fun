# This project serves to play Dota 2 - Dragon Chess mode, which is similar to Candy Crush Saga and other "connect 3 or more gems of same color" games.

# GAME DESCRIPTION (high-level)
# The game is played on a NxN grid, with each gem having one of the X colors.
# The player can move a gem in any of the 4 cardinal directions (up, down, left, right) to a neighboring gem of the same color.
# If the player makes a move that creates a line of 3 or more gems of the same color, the gems are removed from the board and the player earns points.
# The longer the line, the more points the player earns.

# In this project, we need to implement the following:
# 1. Capturing the screenshot of the game window (Dota 2), or simply the whole screen
# 2. Parsing of the screenshot to get the board and the gems on the board.
# 3. A way to represent the board and the gems on the board.
# 4. Algorithm to detect all possible moves that lead to a line of 3 or more gems of the same color.
# 5. Find the best move (highest scoring)
# 6. A way to allow the player to make a move (swap two neighboring gems) by simulating the mouse move - we need a way of mouse simulating that works in Dota 2
# 7. A method that runs the screenshot capture, parsing, move detection, and move execution in time intervals of T milliseconds
# 8. Hotkey to start and stop the main method (that captures the screenshot, parses it, detects the moves, and makes the move), so user can run/stop the script as needed
from enum import StrEnum
import pyautogui
import mss
import cv2
import numpy as np
from PIL import Image
import keyboard
import time
from board import Board
from move_detector import MoveDetector
from move_executor import MoveExecutor
from colors import Color, ColorRange
from config import *


def capture_board_screenshot() -> np.ndarray:
    """Return a screenshot of the board as a numpy array, colors in BGR order (can be indexed like: pixel = array[height][width])"""
    # FIXME tmp debug helper - remove lat
    full_screenshot = cv2.imread('img/screenshot1080p.png')  # BGR order
    return full_screenshot[BOARD_REGION[1]:BOARD_REGION[1]+BOARD_REGION[3], BOARD_REGION[0]:BOARD_REGION[0]+BOARD_REGION[2]]

    with mss.mss() as sct:
        region = {'top': BOARD_REGION[1], 'left': BOARD_REGION[0], 'width': BOARD_REGION[2], 'height': BOARD_REGION[3]}
        screenshot = sct.grab(region)  # ScreenShot object
        return np.array(screenshot)  # BGR order

def parse_board_screenshot(screenshot) -> np.ndarray:
    """Parse the screenshot to get the board state. Return a numpy array of the same size as the board, with each element being the color of the gem or empty string for unknown."""
    # count average color of each gem, but consider only inner area of each gem (exclude 20% of pixels from each side)
    board_state = np.zeros(BOARD_SIZE, dtype=str)
    gem_width, gem_height = GEM_SIZE
    inner_margin = 0.2  # 20% margin from each side

    for row in range(BOARD_SIZE[0]):
        for col in range(BOARD_SIZE[1]):
            print(f'Row: {row}, Col: {col}')
            x_start = int(col * gem_width + gem_width * inner_margin)
            x_end = int((col + 1) * gem_width - gem_width * inner_margin)
            y_start = int(row * gem_height + gem_height * inner_margin)
            y_end = int((row + 1) * gem_height - gem_height * inner_margin)

            gem_area = screenshot[y_start:y_end, x_start:x_end]
            average_color = np.mean(gem_area, axis=(0, 1))  # BGR order
            average_color_rgb = Color(*average_color[::-1])  # Convert BGR to RGB

            # Match the average color to a GemColor
            for gem_color in GemColor:
                color_range = GemColorRanges[gem_color]
                if color_range.contains(average_color_rgb):
                    board_state[row, col] = gem_color.value
                    break
            else:
                print(f"Warning: Unrecognized color {average_color_rgb} at position ({row}, {col})")
                board_state[row, col] = ''
                # TODO debug helper - remove later
                cv2.imshow('unknown', gem_area)
                cv2.waitKey()

    return board_state


def main_loop():
    board = Board(BOARD_SIZE)
    move_detector = MoveDetector()
    move_executor = MoveExecutor()
    sleep_time = SCREENSHOT_INTERVAL / 1000  # seconds
    print("Starting main loop...")
    while True:
        screenshot = capture_board_screenshot()
        cv2.imshow('screenshot', np.array(screenshot))
        cv2.waitKey()
        board_state = parse_board_screenshot(screenshot)
        # TODO continue here tomorrow
        board.update(board_state)
        
        best_move = move_detector.find_best_move(board)
        if best_move:
            move_executor.execute_move(best_move)

        time.sleep(sleep_time)

def on_start():
    print("Starting Dragon Chess bot...")
    main_loop()

def on_stop():
    print("Stopping Dragon Chess bot...")
    # Perform any cleanup if necessary

if __name__ == "__main__":
    keyboard.add_hotkey(HOTKEY_START, on_start)
    keyboard.add_hotkey(HOTKEY_STOP, on_stop)
    print(f"Press {HOTKEY_START} to start the bot, {HOTKEY_STOP} to stop.")
    keyboard.wait()
