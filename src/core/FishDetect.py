import logging
import time

import cv2
import numpy as np
import pyautogui
import matplotlib.pyplot as plt

import os

from ..log import logger

TMP_IMG_DIR = '../img/tmp/'
FISH_POINT_IMG = TMP_IMG_DIR + 'fish_point.png'
FISH_ONBOARD_IMG = TMP_IMG_DIR + 'onboard.png'
FISH_ONBOARD_CMP_IMG = TMP_IMG_DIR + 'onboard_cmp.png'

class FishDetector:

    def __init__(self):
        self.left_top = (700, 80)
        self.width, self.height = (1000, 600)
        self.debug = False
        self.fish_bar_duration = 12

        self._err_sum = 0
        self._err_cnt = 0

    def _clean(self):
        try:
            os.remove(FISH_ONBOARD_IMG)
            os.remove(FISH_ONBOARD_CMP_IMG)

            self._err_sum = 0
            self._err_cnt = 0
        except:
            # logger.error('Clean Img File Error.')
            None

    def _roll(self):
        try:
            os.remove(FISH_ONBOARD_IMG)
            os.rename(FISH_ONBOARD_IMG, FISH_ONBOARD_CMP_IMG)
        except:
            None

    def judge_fish(self, err):
        self._err_sum += err
        self._err_cnt += 1
        if self._err_sum > 0 and self._err_cnt > 10 and err > self._err_sum / self._err_cnt * 8:
            return True
        return False

    def detect_fish_point(self):

        pyautogui.screenshot(FISH_POINT_IMG, region=(self.left_top[0], self.left_top[1], self.width, self.height))

        image = cv2.imread(FISH_POINT_IMG)

        # 转换为灰度图像
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        lines = cv2.HoughLinesP(edges, 2, np.pi / 120, threshold=30, minLineLength=20, maxLineGap=10)

        top_line = None

        # Draw lines and find the endpoint of the fishing line
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]

                if y1 > y2:
                    x1, y1, x2, y2 = x2, y2, x1, y1

                if abs(y1 - y2) < 30 or abs(y1 - y2) / max(abs(x1 - x2), 0.1) < 1 :
                    continue

                if self.debug:
                    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                if top_line is None or top_line[0][1] > y1:
                    top_line = ((x1, y1), (x2, y2))

        if self.debug:
            # Display the result
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title("Detected Fishing Line")
            plt.show()

        if top_line is not None and top_line[0][1] > self.left_top[1] + 10:

            if self.debug:
                logger.debug("Top Line {} - {}".format(top_line[0], top_line[1]))

            return top_line[0][0] + self.left_top[0], top_line[0][1] + self.left_top[1]

        return -1, -1


    def detect_onbard(self, fish_point):

        self._clean()

        start = time.time()

        if fish_point[0] < 0 or fish_point[1] < 0:
            logging.warn("Fish Point {} Invalid!".format(fish_point))
            return False

        while time.time() - start < self.fish_bar_duration:
            x, y = fish_point

            screen_shot = pyautogui.screenshot(FISH_ONBOARD_IMG, region=(int(x - 30), int(y - 30), 60, 60))

            if not os.path.exists(FISH_ONBOARD_IMG):
                logger.error("Img Not Saved!")
                break

            if not os.path.exists(FISH_ONBOARD_CMP_IMG) :
                self._roll()
                continue

            src_img = cv2.imread(FISH_ONBOARD_IMG, cv2.IMREAD_GRAYSCALE)
            cmp_img = cv2.imread(FISH_ONBOARD_CMP_IMG, cv2.IMREAD_GRAYSCALE)

            err = np.sum((src_img.astype("float") - cmp_img.astype("float")) ** 2)
            err /= float(src_img.shape[0] * cmp_img.shape[1])

            if self.debug:
                print("Bar Time: {:.2f} Error Rate: {:.2f}".format(time.time() - start, err))

            if self.judge_fish(err):
                return True

            self._roll()
            time.sleep(0.1)

        return False



if __name__ == '__main__':
    detector = FishDetector()

    point = detector.detect_fish_point()
    detector.detect_onbard(point)
