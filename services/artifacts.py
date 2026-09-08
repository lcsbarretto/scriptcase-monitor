from datetime import datetime

from utils.paths import LOG_DIR as BASE_LOG_DIR
from utils.paths import SCREENSHOT_DIR as BASE_SCREENSHOT_DIR


EXECUTION_ID = None
LOG_DIR = None
SCREENSHOT_DIR = None


def iniciar_execucao():

    global EXECUTION_ID
    global LOG_DIR
    global SCREENSHOT_DIR

    EXECUTION_ID = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S-%f"
    )

    LOG_DIR = BASE_LOG_DIR / EXECUTION_ID
    SCREENSHOT_DIR = BASE_SCREENSHOT_DIR / EXECUTION_ID

    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    SCREENSHOT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


def salvar_screenshot(page, app):

    page.screenshot(
        path=SCREENSHOT_DIR / f"{app}.png",
        full_page=True
    )