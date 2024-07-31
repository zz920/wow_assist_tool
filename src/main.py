import time
import random
from log import logger

from util import KeyPressController, MouseController
from component import FishDetect


if __name__ == "__main__":

    mouse_controller = MouseController.MouseController()
    keyboard_controller = KeyPressController.KeyPressController()

    fish_detect = FishDetect.FishDetector()

    # focus on the first screen
    mouse_controller.move(500, 5)
    mouse_controller.left_click()

    mouse_controller.move(500 + random.randint(1, 100), 500 + random.randint(1, 100))
    mouse_controller.left_click()

    failure_cnt = 0
    while failure_cnt < 11:

        # press 1 start fishing
        keyboard_controller.press('1')
        mouse_controller.move_to_random_position((1750, 780))

        # time.sleep(random.randint(1, 30) / 100)

        mouse_position = fish_detect.detect_fish_point()
        if mouse_position[0] < 0 or mouse_position[1] < 0:
            print("Fish Point not Found!")
            # keyboard_controller.press('space')
            failure_cnt += 1
            continue
        else:
            print("Found Fish Point at {}".format(mouse_position))

        mouse_controller.move_to_random_position()

        failure_cnt = 0
        if fish_detect.detect_onbard(mouse_position):
            # time.sleep(0.27 + random.randint(1, 20) / 100)
            print("Fish Detected!")
        else:
            print("No Fish Detected!")
            # keyboard_controller.press('space')
            # time.sleep(1.9 + random.randint(1, 30) / 100)
            continue

        mouse_controller.move(*mouse_position)
        time.sleep(random.randint(10, 15) / 100)
        mouse_controller.right_click()
        time.sleep(1 + random.randint(30, 50) / 100)
