from pathlib import Path
import sys


if getattr(sys, "frozen", False):

    # Programa compilado pelo PyInstaller.
    # As configurações ficam ao lado do executável.
    ROOT = Path(sys.executable).resolve().parent

else:

    # Execução normal pelo Python.
    ROOT = Path(__file__).resolve().parent.parent


CONFIG_DIR = ROOT / "config"

LOG_DIR = ROOT / "logs"

SCREENSHOT_DIR = ROOT / "screenshots"