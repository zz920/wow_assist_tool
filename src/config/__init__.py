from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent.absolute().__str__()

# img settings
TMP_IMG_DIR = PROJECT_ROOT_DIR + '/img/tmp/'
FISH_POINT_IMG = TMP_IMG_DIR + 'fish_point.png'
FISH_ONBOARD_IMG = TMP_IMG_DIR + 'onboard.png'
FISH_ONBOARD_CMP_IMG = TMP_IMG_DIR + 'onboard_cmp.png'


LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LOG_DATE_FORMAT = '%b %d %H:%M:%S'
LOG_FILENAME = PROJECT_ROOT_DIR + '/log/info.log'