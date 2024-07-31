import pyautogui

from ..log import logger


class KeyPressController:

    def __init__(self):
        None

    def press(self, key):
        logger.debug("Press {} key".format(key))
        pyautogui.press(key)
