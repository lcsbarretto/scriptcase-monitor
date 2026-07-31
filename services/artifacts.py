from datetime import datetime
from pathlib import Path
from utils.paths import LOG_DIR, SCREENSHOT_DIR


EXECUTION_ID = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

LOG_DIR = Path("logs") / EXECUTION_ID
SCREENSHOT_DIR = Path("screenshots") / EXECUTION_ID

LOG_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


def salvar_screenshot(page, app):

    page.screenshot(
        path=SCREENSHOT_DIR / f"{app}.png",
        full_page=True
    )