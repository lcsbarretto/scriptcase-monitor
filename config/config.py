from configparser import ConfigParser
from pathlib import Path
from utils.paths import CONFIG_DIR


config = ConfigParser()
config.read(CONFIG_DIR / "config.ini", encoding="utf-8")

cfg = config["SCRIPTCASE"]

URL = cfg["URL"]
BASE_URL = cfg["BASE_URL"]
APP_PATH = cfg["APP_PATH"]

USUARIO = cfg["USUARIO"]
SENHA = cfg["SENHA"]

HEADLESS = cfg.getboolean("HEADLESS", fallback=True)
TIMEOUT = cfg.getint("TIMEOUT", fallback=10000)
