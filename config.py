import pyautogui
from enum import StrEnum

from colors import Color, ColorRange


DEBUG_MODE = True  # if enabled, some debug info will be printed, some images displayed (e.g. if a screenshot is captured), etc.

HOTKEY_START = 'f7'  # start the main loop
HOTKEY_STOP = 'f8'  # stop the main loop
HOTKEY_EXIT = 'esc'  # quit the program (if the main loop is not running)
HOTKEY_KILL = 'f9'  # Emergency button: hard-kill the program including debug windows etc
SCREENSHOT_INTERVAL = 1000  # milliseconds
BOARD_REGION = (220, 130, 720, 720)  # (left, top, width, height)
BOARD_SIZE = (8, 8)  # number of columns and rows (width, height)

GEM_SIZE = (BOARD_REGION[2] // BOARD_SIZE[0], BOARD_REGION[3] // BOARD_SIZE[1])  # width, height
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

class GemColor(StrEnum):
    red = 'red'
    red_special = 'red_special'
    dark_red = 'dark_red'
    dark_red_special = 'dark_red_special'
    blue = 'blue'
    blue_special = 'blue_special'
    turquoise = 'turquoise'
    turquoise_special = 'turquoise_special'
    yellow = 'yellow'
    yellow_special = 'yellow_special'
    pink = 'pink'
    pink_special = 'pink_special'

GemColorRanges = {
    GemColor.red: ColorRange(Color(170, 60, 40), Color(200, 90, 60)),
    GemColor.red_special: ColorRange(Color(0, 0, 0), Color(0, 0, 0)),
    GemColor.dark_red: ColorRange(Color(60, 20, 25), Color(80, 30, 35)),
    GemColor.dark_red_special: ColorRange(Color(0, 0, 0), Color(0, 0, 0)),
    GemColor.blue: ColorRange(Color(70, 80, 150), Color(80, 95, 180)),
    GemColor.blue_special: ColorRange(Color(0, 0, 0), Color(0, 0, 0)),
    GemColor.turquoise: ColorRange(Color(60, 140, 150), Color(75, 160, 165)),
    GemColor.turquoise_special: ColorRange(Color(0, 0, 0), Color(0, 0, 0)),
    GemColor.yellow: ColorRange(Color(190, 145, 110), Color(215, 170, 120)),
    GemColor.yellow_special: ColorRange(Color(0, 0, 0), Color(0, 0, 0)),
    GemColor.pink: ColorRange(Color(125, 65, 140), Color(185, 115, 195)),
    GemColor.pink_special: ColorRange(Color(0, 0, 0), Color(0, 0, 0))
}


################################################## AUTOMATED CHECKS ##################################################
# check that all gem colors are defined in GemColorRange
if len(GemColorRanges) != len(GemColor):
    raise ValueError(f"Not all gem colors are defined in GemColorRange. Please fix the GemColorRange in {__file__}.")

# check that no two gem colors have overlapping ranges, because then the color detection would not work properly
for color_range in GemColorRanges.values():
    for other_color_range in GemColorRanges.values():
        if color_range == other_color_range:
            continue
        if color_range.has_intersection(other_color_range):
            raise ValueError(f"Color range {color_range} has intersection with {other_color_range}. Please fix the color ranges in {__file__}.")
