from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# img settings
TMP_IMG_DIR = PROJECT_ROOT_DIR.joinpath('img').joinpath('tmp')
FISH_POINT_IMG = TMP_IMG_DIR.joinpath('fish_point.png')
FISH_ONBOARD_IMG = TMP_IMG_DIR.joinpath('onboard.png')
FISH_ONBOARD_CMP_IMG = TMP_IMG_DIR.joinpath('onboard_cmp.png')


LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LOG_DATE_FORMAT = '%b %d %H:%M:%S'
LOG_FILENAME = PROJECT_ROOT_DIR.joinpath('log').joinpath('info.log')