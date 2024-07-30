import time

import cv2
import numpy as np
import pyautogui
import matplotlib.pyplot as plt

import os

class FishDetector:

    def __init__(self):
        self.left_top = (700, 80)
        self.width, self.height = (1000, 600)
        self.debug = False
        self.fish_bar_duration = 12

    def detect_fish_point(self):

        screen_shot = pyautogui.screenshot('fish_point.png', region=(self.left_top[0], self.left_top[1], self.width, self.height))

        image = cv2.imread('fish_point.png')

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

                # print("find line from: ({}), to ({})".format((x1, y1), (x2, y2)))

                if top_line is None or top_line[0][1] > y1:
                    top_line = ((x1, y1), (x2, y2))

        if self.debug:
            # Display the result
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.title("Detected Fishing Line")
            plt.show()

        if top_line is not None and top_line[0][1] > self.left_top[1] + 10:
            if self.debug:
                print("top line from: ({}), to ({})".format(top_line[0], top_line[1]))
            return top_line[0][0] + self.left_top[0], top_line[0][1] + self.left_top[1]

        return -1, -1


    def detect_onbard(self, fish_point):
        try:
            os.remove("onboard_cmp.png")
        except(Exception):
            None

        start = time.time()

        if fish_point[0] < 0 or fish_point[1] < 0:
            print("point invalid! {}".format(fish_point))
            return False

        err_sum = 0
        cnt = 0
        avg_err = 0

        while time.time() - start < self.fish_bar_duration:
            x, y = fish_point

            screen_shot = pyautogui.screenshot('onboard.png', region=(int(x - 30), int(y - 30), 60, 60))

            if not os.path.exists("./onboard.png"):
                print("Fatal error, screen shot not saved")
                break

            if os.path.exists("./onboard.png") and not os.path.exists("./onboard_cmp.png") :
                os.rename("onboard.png", "onboard_cmp.png")
                # print("cmp file not exist")
                continue

            src_img = cv2.imread('onboard.png', cv2.IMREAD_GRAYSCALE)
            cmp_img = cv2.imread('onboard_cmp.png', cv2.IMREAD_GRAYSCALE)

            err = np.sum((src_img.astype("float") - cmp_img.astype("float")) ** 2)
            err /= float(src_img.shape[0] * cmp_img.shape[1])

            if self.debug:
                print("{:.2f} Error: {:.2f}".format(time.time() - start, err))

            if err_sum > 0 and cnt > 10 and err > err_sum / cnt * 8:
            # if err_sum > 500:
                return True

            err_sum += err
            cnt += 1

            try:
                os.remove("onboard_cmp.png")
                os.rename("onboard.png", "onboard_cmp.png")
            except(Exception):
                None

            time.sleep(0.1)

        return False



if __name__ == '__main__':
    detector = FishDetector()

    point = detector.detect_fish_point()
    detector.detect_onbard(point)
