import sys
import cv2
import numpy as np
import pyautogui
from typing import Optional, Tuple

class ImageAreaSelector:
    def __init__(self, image_path: Optional[str] = None):
        self.image = self.load_image(image_path)
        self.original_image = self.image.copy()
        self.window_name = "Image Area Selector"
        self.start_point = None
        self.end_point = None
        self.zoomed = False
        self.zoom_factor = 1.0
        self.zoom_offset = (0, 0)
        self.rmb_first_point = None
        self.selected_rectangle = None

    def load_image(self, image_path: Optional[str]) -> np.ndarray:
        if image_path:
            return cv2.imread(image_path)
        return np.array(pyautogui.screenshot())

    def mouse_callback(self, event: int, x: int, y: int, flags: int, param: None) -> None:
        image_x, image_y = self.screen_to_image_coords(x, y)
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_point = (image_x, image_y)
            self.selected_rectangle = None
        elif event == cv2.EVENT_LBUTTONUP:
            self.end_point = (image_x, image_y)
            self.print_rectangle_info()
            self.selected_rectangle = (self.start_point, self.end_point)
            self.start_point = None
            self.end_point = None
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.rmb_first_point is None:
                self.rmb_first_point = (image_x, image_y)
                self.selected_rectangle = None
            else:
                self.start_point = self.rmb_first_point
                self.end_point = (image_x, image_y)
                self.print_rectangle_info()
                self.selected_rectangle = (self.start_point, self.end_point)
                self.rmb_first_point = None
                self.start_point = None
                self.end_point = None
        elif event == cv2.EVENT_MOUSEWHEEL:
            if flags > 0:
                self.zoom_in(image_x, image_y)
            else:
                self.zoom_out(image_x, image_y)

    def screen_to_image_coords(self, x: int, y: int) -> Tuple[int, int]:
        if self.zoomed:
            image_x = int(self.zoom_offset[0] + x / self.zoom_factor)
            image_y = int(self.zoom_offset[1] + y / self.zoom_factor)
        else:
            image_x, image_y = x, y
        return image_x, image_y

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
            center_x, center_y = x, y
            
            left = max(0, int(center_x - width / (2 * self.zoom_factor)))
            top = max(0, int(center_y - height / (2 * self.zoom_factor)))
            right = min(width, int(center_x + width / (2 * self.zoom_factor)))
            bottom = min(height, int(center_y + height / (2 * self.zoom_factor)))
            
            self.zoom_offset = (left, top)
            self.image = cv2.resize(self.original_image[top:bottom, left:right], (width, height))
        else:
            self.image = self.original_image.copy()
            self.zoom_offset = (0, 0)

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
                start_x, start_y = self.start_point
                cv2.circle(display_image, (int((start_x - self.zoom_offset[0]) * self.zoom_factor),
                                           int((start_y - self.zoom_offset[1]) * self.zoom_factor)), 3, (0, 255, 0), -1)
            
            if self.start_point and self.end_point:
                start_x, start_y = self.start_point
                end_x, end_y = self.end_point
                cv2.rectangle(display_image, 
                              (int((start_x - self.zoom_offset[0]) * self.zoom_factor),
                               int((start_y - self.zoom_offset[1]) * self.zoom_factor)),
                              (int((end_x - self.zoom_offset[0]) * self.zoom_factor),
                               int((end_y - self.zoom_offset[1]) * self.zoom_factor)),
                              (0, 255, 0), 2)

            if self.rmb_first_point:
                rmb_x, rmb_y = self.rmb_first_point
                cv2.circle(display_image, (int((rmb_x - self.zoom_offset[0]) * self.zoom_factor),
                                           int((rmb_y - self.zoom_offset[1]) * self.zoom_factor)), 3, (0, 0, 255), -1)

            if self.selected_rectangle:
                start_x, start_y = self.selected_rectangle[0]
                end_x, end_y = self.selected_rectangle[1]
                cv2.rectangle(display_image,
                              (int((start_x - self.zoom_offset[0]) * self.zoom_factor),
                               int((start_y - self.zoom_offset[1]) * self.zoom_factor)),
                              (int((end_x - self.zoom_offset[0]) * self.zoom_factor),
                               int((end_y - self.zoom_offset[1]) * self.zoom_factor)),
                              (0, 255, 0), 2)

            mouse_pos = pyautogui.position()
            window_pos = cv2.getWindowImageRect(self.window_name)
            if window_pos:
                relative_x = mouse_pos.x - window_pos[0]
                relative_y = mouse_pos.y - window_pos[1]
                image_x, image_y = self.screen_to_image_coords(relative_x, relative_y)
                cv2.putText(display_image, f"Image coords: {image_x}, {image_y}", (10, 30),
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
