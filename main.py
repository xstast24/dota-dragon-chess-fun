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
from contextlib import suppress
from enum import StrEnum
import mss
import cv2
import mss.screenshot
import numpy as np
import time
from board import Board
from move_calculator import MoveCalculator
from move_executor import MoveExecutor
from config import *
from threading import Event
from hotkeys import add_hotkey, start_listening, stop_listening


run_condition = Event()  # used to start/stop the game execution loop
exit_condition = Event()  # used to exit the whole program completely


def capture_board_screenshot() -> np.ndarray:
    """Return a screenshot of the board as a numpy array, colors in RGB order (can be indexed like: pixel = array[height][width])"""
    # debug help - load img from file - uncomment if needed
    # full_screenshot = cv2.imread('img/screen2.png')  # BGR order
    # full_screenshot = cv2.cvtColor(full_screenshot, cv2.COLOR_BGR2RGB)
    # return full_screenshot[BOARD_REGION[1]:BOARD_REGION[1]+BOARD_REGION[3], BOARD_REGION[0]:BOARD_REGION[0]+BOARD_REGION[2]]

    with mss.mss() as sct:
        region = {'top': BOARD_REGION[1], 'left': BOARD_REGION[0], 'width': BOARD_REGION[2], 'height': BOARD_REGION[3]}
        screenshot: mss.screenshot.ScreenShot = sct.grab(region)  # ScreenShot object
        np_screenshot = np.array(screenshot)
        rgb_screenshot = cv2.cvtColor(np_screenshot, cv2.COLOR_BGR2RGB)
        return rgb_screenshot

def main_loop():
    board = Board(BOARD_SIZE)
    move_calculator = MoveCalculator()
    move_executor = MoveExecutor()
    sleep_time = SCREENSHOT_INTERVAL / 1000  # seconds

    print("Starting main loop...")
    while run_condition.is_set():
        screenshot = capture_board_screenshot()
        if DEBUG_MODE:
            print("Captured new screenshot, showing it...")
            cv2.imshow('screenshot', cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR))
            cv2.waitKey()
        board.update_from_screenshot(screenshot)
        if DEBUG_MODE:
            print(board)

        best_move = move_calculator.find_longest_sequence_move(board)
        if best_move:
            print(f"Executing move: {best_move}")
            move_executor.execute_move(best_move)

        time.sleep(sleep_time)

def start():
    if not run_condition.is_set():
        print("Starting...")
        run_condition.set()
        main_loop()
    else:
        print("Already running")

def stop():
    print("Stopping...")
    run_condition.clear()

def exit():
    print("Exiting the program")
    run_condition.clear()
    with suppress(Exception):
        cv2.destroyAllWindows()
    exit_condition.set()


if __name__ == "__main__":
    add_hotkey(HOTKEY_START, start)
    add_hotkey(HOTKEY_STOP, stop)
    add_hotkey(HOTKEY_KILL, exit)
    print(f"Press {HOTKEY_START} to start the bot, {HOTKEY_STOP} to stop.")
    print(f"Press {HOTKEY_KILL} to exit the program.")
    start_listening()
    try:
        while not exit_condition.is_set():
            time.sleep(0.2)  # Small sleep to prevent high CPU usage
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
    finally:
        stop_listening()
        print("Program terminated")
