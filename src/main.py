from src.log import logger
from src.core import AutoFishPlugin

if __name__ == "__main__":
    logger.info("----- Assist Tool Start -----")
    task = AutoFishPlugin()
    task.run(None)
    logger.info("----- Assist Tool End -----")
