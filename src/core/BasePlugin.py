from ..util.MouseController import  MouseController
from ..util.KeyPressController import KeyPressController
from ..log import logger

class BasePlugin:

    def __init__(self):
        self.mouseController = MouseController()
        self.keyPressController = KeyPressController()
        self.logger = logger

    def run(self, context):
        raise NotImplementedError

    def summary(self, context):
        raise NotImplementedError
