import pyautogui
from enum import StrEnum

from colors import Color, ColorRange


DEBUG_MODE = True  # if enabled, some debug info will be printed, some images displayed (e.g. if a screenshot is captured), etc.

HOTKEY_START = 'f7'
HOTKEY_STOP = 'f8'
SCREENSHOT_INTERVAL = 100  # milliseconds
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
    GemColor.red: ColorRange(Color(170, 60, 40), Color(195, 90, 60)),
    GemColor.red_special: ColorRange(Color(255, 0, 0), Color(255, 50, 50)),
    GemColor.dark_red: ColorRange(Color(60, 20, 25), Color(80, 30, 35)),
    GemColor.dark_red_special: ColorRange(Color(255, 0, 0), Color(255, 50, 50)),
    GemColor.blue: ColorRange(Color(70, 80, 150), Color(80, 95, 165)),
    GemColor.blue_special: ColorRange(Color(0, 0, 255), Color(50, 50, 255)),
    GemColor.turquoise: ColorRange(Color(60, 140, 150), Color(75, 160, 165)),
    GemColor.turquoise_special: ColorRange(Color(0, 255, 255), Color(50, 255, 255)),
    GemColor.yellow: ColorRange(Color(190, 145, 110), Color(215, 170, 120)),
    GemColor.yellow_special: ColorRange(Color(255, 255, 0), Color(255, 255, 50)),
    GemColor.pink: ColorRange(Color(160, 85, 170), Color(180, 110, 190)),
    GemColor.pink_special: ColorRange(Color(255, 105, 180), Color(255, 150, 230))
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
