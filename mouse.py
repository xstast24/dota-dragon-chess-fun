import pyautogui
import time
import win32api
import win32con


class Mouse:
    @staticmethod
    def move(x: int, y: int, duration: float = 0.2):
        """
        Move the cursor to the specified coordinates.
        
        :param x: X-coordinate on the screen
        :param y: Y-coordinate on the screen
        :param duration: Time taken to move the cursor (in seconds)
        """
        pyautogui.moveTo(x, y, duration=duration)

    @staticmethod
    def click(x: int, y: int, duration: float = 0.1):
        """
        Perform a click at the specified coordinates.
        
        :param x: X-coordinate on the screen
        :param y: Y-coordinate on the screen
        :param duration: Time taken to click (in seconds)
        """
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(duration)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    @staticmethod
    def move_and_click(x: int, y: int, move_duration: float = 0.2, click_duration: float = 0.1):
        """
        Move the cursor to the specified coordinates and perform a click.
        
        :param x: X-coordinate on the screen
        :param y: Y-coordinate on the screen
        :param move_duration: Time taken to move the cursor (in seconds)
        :param click_duration: Time taken to click (in seconds)
        """
        pyautogui.moveTo(x, y, duration=move_duration)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(click_duration)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

    @staticmethod
    def drag(start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.2):
        """
        Simulate a mouse drag from the start point to the end point.
        
        :param start_x: Starting X-coordinate
        :param start_y: Starting Y-coordinate
        :param end_x: Ending X-coordinate
        :param end_y: Ending Y-coordinate
        :param duration: Time taken for the drag operation (in seconds)
        """
        pyautogui.moveTo(start_x, start_y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, start_x, start_y, 0, 0)
        time.sleep(0.1)
        
        steps = 20
        for i in range(1, steps + 1):
            x = start_x + (end_x - start_x) * i // steps
            y = start_y + (end_y - start_y) * i // steps
            win32api.SetCursorPos((x, y))
            time.sleep(duration / steps)
        
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, end_x, end_y, 0, 0)


if __name__ == "__main__":
    print("Starting simple click & drag in 5 seconds...")
    time.sleep(5)
    print("Starting...")
    Mouse.move_and_click(965, 785)
    time.sleep(1)
    Mouse.drag(450, 350, 550, 350, duration=0.5)
    print("Done")
