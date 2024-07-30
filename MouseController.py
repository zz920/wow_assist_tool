import pyautogui
import time
import random

import threading

class MouseController:

    def __init__(self):
        self._offset = 7
        self.time_seg = 0.01
        self.screen_x, self.screen_y = pyautogui.size()

        print("Screen Info: ", pyautogui.size())

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
        return mouse_x, mouse_y, abs(x - mouse_x) > self._offset or abs(y - mouse_y) > self._offset

    def move(self, x, y, func=pyautogui.easeOutQuad):
        mouse_x, mouse_y, _ = self._check_postion(0, 0)

        distance_x, distance_y = abs(x - mouse_x), abs(y - mouse_y)
        distance = pow(distance_x ** 2 + distance_y ** 2, 0.5)

        duration = distance / 4357
        offset = random.randint(1, 40) / 100
        pyautogui.moveTo(x, y, duration + offset, func)

        # print("move mouse to:({}, {})".format(x, y))

    def left_click(self):
        pyautogui.click(button='left')

    def right_click(self):
        pyautogui.click(button='right')

    def move_to_random_position(self, point=None):
        if point is None:
            random_x, random_y = random.randint(100, self.screen_x), random.randint(100, self.screen_y)
        else:
            random_x, random_y = random.randint(-100, 100) + point[0], random.randint(-100, 100) + point[1]
        self.move(random_x, random_y, pyautogui.easeInBounce)
