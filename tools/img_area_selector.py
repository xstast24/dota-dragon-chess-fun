import sys
import cv2
import numpy as np
import pyautogui
from typing import Optional

class ImageAreaSelector:
    def __init__(self, image_path: Optional[str] = None):
        self.image = self.load_image(image_path)
        self.original_image = self.image.copy()
        self.window_name = "Image Area Selector"
        self.start_point = None
        self.end_point = None
        self.zoomed = False
        self.zoom_factor = 1.0
        self.rmb_first_point = None
        self.selected_rectangle = None

    def load_image(self, image_path: Optional[str]) -> np.ndarray:
        if image_path:
            return cv2.imread(image_path)
        return np.array(pyautogui.screenshot())

    def mouse_callback(self, event: int, x: int, y: int, flags: int, param: None) -> None:
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_point = (x, y)
            self.selected_rectangle = None
        elif event == cv2.EVENT_LBUTTONUP:
            self.end_point = (x, y)
            self.print_rectangle_info()
            self.selected_rectangle = (self.start_point, self.end_point)
            self.start_point = None
            self.end_point = None
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.rmb_first_point is None:
                self.rmb_first_point = (x, y)
                self.selected_rectangle = None
            else:
                self.start_point = self.rmb_first_point
                self.end_point = (x, y)
                self.print_rectangle_info()
                self.selected_rectangle = (self.start_point, self.end_point)
                self.rmb_first_point = None
                self.start_point = None
                self.end_point = None
        elif event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                self.zoom_in(x, y)
            else:
                self.zoom_out(x, y)

    def zoom_in(self, x: int, y: int) -> None:
        self.zoom_factor *= 1.1
        self.zoomed = True
        self.update_zoomed_image(x, y)

    def zoom_out(self, x: int, y: int) -> None:
        self.zoom_factor /= 1.1
        if self.zoom_factor < 1.0:
            self.zoom_factor = 1.0
            self.zoomed = False
        self.update_zoomed_image(x, y)

    def update_zoomed_image(self, x: int, y: int) -> None:
        if self.zoomed:
            height, width = self.original_image.shape[:2]
            center_x, center_y = int(x / self.zoom_factor), int(y / self.zoom_factor)
            
            left = max(0, center_x - int(width / (2 * self.zoom_factor)))
            top = max(0, center_y - int(height / (2 * self.zoom_factor)))
            right = min(width, center_x + int(width / (2 * self.zoom_factor)))
            bottom = min(height, center_y + int(height / (2 * self.zoom_factor)))
            
            self.image = cv2.resize(self.original_image[top:bottom, left:right], (width, height))
        else:
            self.image = self.original_image.copy()

    def print_rectangle_info(self) -> None:
        if self.start_point and self.end_point:
            x1, y1 = self.start_point
            x2, y2 = self.end_point
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            print(f"Rectangle: Point1({x1}, {y1}), Point2({x2}, {y2}), Width: {width}, Height: {height}")

    def run(self) -> None:
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)

        print("Controls:")
        print("- Left Mouse Button: Click and drag to select rectangle area")
        print("- Right Mouse Button: Click once to set point1, click again to set point2 of rectangle area")
        print("- Mouse Wheel: Zoom in/out")
        print("- ESC: Exit")

        while True:
            display_image = self.image.copy()
            
            if self.start_point:
                cv2.circle(display_image, self.start_point, 3, (0, 255, 0), -1)
            
            if self.start_point and self.end_point:
                cv2.rectangle(display_image, self.start_point, self.end_point, (0, 255, 0), 2)

            if self.rmb_first_point:
                cv2.circle(display_image, self.rmb_first_point, 3, (0, 0, 255), -1)

            if self.selected_rectangle:
                cv2.rectangle(display_image, self.selected_rectangle[0], self.selected_rectangle[1], (0, 255, 0), 2)

            mouse_pos = pyautogui.position()
            cv2.putText(display_image, f"Mouse: {mouse_pos.x}, {mouse_pos.y}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow(self.window_name, display_image)

            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break

        cv2.destroyAllWindows()

def main(image_path: Optional[str] = None) -> None:
    selector = ImageAreaSelector(image_path)
    selector.run()

if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    main(image_path)
