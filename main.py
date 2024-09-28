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
