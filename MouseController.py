import pyautogui
import time
import random

import threading

class MouseController:

    def __init__(self):
        self._thread = threading.Thread(target=self.report())
        self.time_seg = 0.01
        self._thread.start()
        self._offset = 10;

    def report(self):
        last_x, last_y, _ = self._check_postion(0, 0);
        while True:
            mouse_x, mouse_y, move_flg = self._check_postion(last_x, last_y)
            if move_flg:
                print("move mouse to:({}, {})".format(mouse_x, mouse_y))
                last_x, last_y = mouse_x, mouse_y
            time.sleep(self.time_seg)

    def _check_postion(self, x, y):
        mouse_x, mouse_y = pyautogui.position()
        return mouse_x, mouse_y, abs(x - mouse_x) > self._offset or abs(y - mouse_y) > self._offset;

    def mock_real_move(self, x, y):
        mouse_x, mouse_y, _ = self._check_postion(0, 0);
