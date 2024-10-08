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

import time
from threading import Event

import cv2
import keyboard
import mss
import mss.screenshot
import numpy as np

from board import Board
from config import *
from move_calculator import MoveCalculator
from move_executor import MoveExecutor

run_condition = Event()  # used to turn the main loop on/off


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
    global run_condition
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


def on_start():
    global run_condition
    if not run_condition.is_set():
        print("Starting the loop...")
        run_condition.set()
        main_loop()


def on_stop():
    print("Stopping the loop...")
    global run_condition
    run_condition.clear()


def hard_kill():
    print("Killing the script...")
    run_condition.clear()
    cv2.destroyAllWindows()
    exit()


if __name__ == "__main__":
    # if not pyuac.isUserAdmin():
    #     print("Re-launching as admin")
    #     pyuac.runAsAdmin()
    # else:        
    #     print('Running as admin')  # Already an admin here.
    keyboard.add_hotkey(HOTKEY_START, on_start)
    keyboard.add_hotkey(HOTKEY_STOP, on_stop)
    keyboard.add_hotkey(HOTKEY_KILL, hard_kill)
    print(f"Press {HOTKEY_START} to start the bot, {HOTKEY_STOP} to stop.")
    keyboard.wait(HOTKEY_EXIT)  # escape kills the program completely
