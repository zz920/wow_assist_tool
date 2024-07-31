import random
import time

from src.core.FishDetect import FishDetector
from src.core.BasePlugin import BasePlugin


class AutoFishPlugin(BasePlugin):

    def __init__(self):
        self.name = "AutoFishPlugin"
        self.fishDetector = FishDetector()

        self._failureCnt = 0
        self._successCnt = 0
        self._executionCnt = 0
        self._start_time = 0

        super().__init__()

    def focus_on_window(self):
        # focus on the first screen
        self.mouseController.move(500 + random.randint(1, 100), 500 + random.randint(1, 100))
        self.mouseController.left_click()

    def start_fishing(self):
        # press 1 start fishing
        self.keyPressController.press('1')
        self.mouseController.move_to_random_position((1750, 780))

    def find_fish_point(self):
        fishPoint = self.fishDetector.detect_fish_point()
        if self.mouseController.is_out_of_screen(fishPoint):
            self.logger.warn("Fish Point not Found!")
            return None

        self.logger.info("Found Fish Point at {}".format(fishPoint))
        self.mouseController.move_to_random_position()
        return fishPoint

    def monitor_fishing(self, position):
        if self.fishDetector.detect_onbard(position):
            self.logger.info("Fish Detected!")
            return True

        self.logger.warn("No Fish Detected!")
        return False

    def harvest_fish(self, position):
        self.mouseController.move(*position)
        time.sleep(random.randint(10, 15) / 100)
        self.mouseController.right_click()
        time.sleep(1 + random.randint(30, 50) / 100)

    def reset_counter(self):
        self._failureCnt = 0
        self._successCnt = 0
        self._start_time = time.time()
        self._executionCnt = 0

    def run(self, context):
        self.logger.info("Plugin: {} running...".format(self.name))

        self.mouseController.move(500, 5)
        self.mouseController.left_click()

        self.focus_on_window()
        self.reset_counter()

        while self._failureCnt < 11:
            self._executionCnt += 1
            self.start_fishing()
            # time.sleep(random.randint(1, 30) / 100)

            fishPoint = self.find_fish_point()
            if fishPoint is None:
                self._failureCnt += 1
                continue
            else:
                self._failureCnt = 0

            if self.monitor_fishing(fishPoint):
                self.harvest_fish(fishPoint)
                self._successCnt += 1

        self.logger.info("Plugin: {} end.".format(self.name))

        self.summary(None, "")

    def summary(self, context, message):
        self.logger.info("AutoFishPlugin Summary: ")
        self.logger.info("      Execute Count: {}".format(self._executionCnt))
        self.logger.info("      Success Count: {}".format(self._successCnt))
        self.logger.info("      Total Time: {.2f} sec\n".format(time.time() - self._start_time))
