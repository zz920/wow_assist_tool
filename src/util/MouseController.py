import pyautogui
import time
import random

from ..log import logger


class MouseController:

    def __init__(self):
        self._offset = 7
        self.time_seg = 0.01
        self.screen_x, self.screen_y = pyautogui.size()

        logger.debug("Screen Info: {}".format(pyautogui.size()))

    def _check_position(self, point):
        mouse_x, mouse_y = pyautogui.position()
        return mouse_x, mouse_y, abs(point[0] - mouse_x) > self._offset or abs(point[1] - mouse_y) > self._offset

    def is_out_of_screen(self, point):
        return (len(point) == 2
                and point[0] < self.screen_x
                and point[1] < self.screen_y
                and point[0] > 0 and point[1] > 0)


    def report(self):
        last_x, last_y, _ = self._check_position((0, 0))
        while True:
            mouse_x, mouse_y, move_flg = self._check_position((last_x, last_y))
            if move_flg:
                logger.debug("Move Mouse to: {}".format((mouse_x, mouse_y)))
                last_x, last_y = mouse_x, mouse_y
            time.sleep(self.time_seg)

    def move(self, x, y, func=pyautogui.easeOutQuad):
        mouse_x, mouse_y, _ = self._check_position((0, 0))

        distance_x, distance_y = abs(x - mouse_x), abs(y - mouse_y)
        distance = pow(distance_x ** 2 + distance_y ** 2, 0.5)

        duration = distance / 4357
        offset = random.randint(1, 40) / 100
        pyautogui.moveTo(x, y, duration + offset, func)

    def move_to_random_position(self, point=None):
        if point is None:
            random_x, random_y = random.randint(100, self.screen_x), random.randint(100, self.screen_y)
        else:
            random_x, random_y = random.randint(-100, 100) + point[0], random.randint(-100, 100) + point[1]
        self.move(random_x, random_y, pyautogui.easeInBounce)

    def left_click(self):
        pyautogui.click(button='left')
        logger.debug("Click left mouse")

    def right_click(self):
        pyautogui.click(button='right')
        logger.debug("Click right mouse")
