from __future__ import annotations

from random import randint
from typing import Tuple


class Color:
    def __init__(self, red: int | float, green: int | float, blue: int | float):
        """Color class for convenient usage of colors. Values can be <0;255> int or float (floats are rounded to closest int)."""
        self.red = self._clip_to_rgb_range(round(red))
        self.green = self._clip_to_rgb_range(round(green))
        self.blue = self._clip_to_rgb_range(round(blue))

    @classmethod
    def from_bgr_tuple(cls, bgr: Tuple[int, int, int]) -> Color:
        return cls(red=bgr[2], green=bgr[1], blue=bgr[0])

    @classmethod
    def from_rgb_tuple(cls, rgb: Tuple[int, int, int]) -> Color:
        return cls(red=rgb[0], green=rgb[1], blue=rgb[2])

    @staticmethod
    def random_color() -> Color:
        return Color(red=randint(0, 255), green=randint(0, 255), blue=randint(0, 255))

    @staticmethod
    def _clip_to_rgb_range(value: int) -> int:
        return max(0, min(255, value))

    def as_rgb_tuple(self) -> Tuple[int, int, int]:
        return self.red, self.green, self.blue

    def as_bgr_tuple(self) -> Tuple[int, int, int]:
        """Can be used in OpenCV functions."""
        return self.blue, self.green, self.red

    def as_rgb_hex(self, use_hash: bool = True) -> str:
        """Return color as hexadecimal #RRGGBB - missing values are padded with 0. Leading hash is optional."""
        return f'{"#" if use_hash else ""}{self.red:02x}{self.green:02x}{self.blue:02x}'

    def as_bgr_hex(self, use_hash: bool = True) -> str:
        """Return color as hexadecimal #BBGGRR - missing values are padded with 0. Leading hash is optional."""
        return f'{"#" if use_hash else ""}{self.blue:02x}{self.green:02x}{self.red:02x}'

    def __str__(self) -> str:
        return f"Color(r={self.red}, g={self.green}, b={self.blue})"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other: Color) -> bool:
        return self.red == other.red and self.green == other.green and self.blue == other.blue


class ColorRange:
    def __init__(self, min_rgb: Color, max_rgb: Color) -> None:
        self.min_rgb = min_rgb
        self.max_rgb = max_rgb

    def contains(self, color: Color) -> bool:
        return self.min_rgb.red <= color.red <= self.max_rgb.red and \
               self.min_rgb.green <= color.green <= self.max_rgb.green and \
               self.min_rgb.blue <= color.blue <= self.max_rgb.blue

    def has_intersection(self, other: ColorRange) -> bool:
        return self.min_rgb.red <= other.max_rgb.red and self.max_rgb.red >= other.min_rgb.red and \
               self.min_rgb.green <= other.max_rgb.green and self.max_rgb.green >= other.min_rgb.green and \
               self.min_rgb.blue <= other.max_rgb.blue and self.max_rgb.blue >= other.min_rgb.blue

    def __str__(self) -> str:
        return f"ColorRange(min_rgb={self.min_rgb}, max_rgb={self.max_rgb})"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other: ColorRange) -> bool:
        return self.min_rgb == other.min_rgb and self.max_rgb == other.max_rgb
