from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini", encoding="utf-8")

cfg = config["SCRIPTCASE"]

URL = cfg["URL"]
APP_PATH = cfg["APP_PATH"]
BASE_URL = cfg["BASE_URL"]
USUARIO = cfg["USUARIO"]
SENHA = cfg["SENHA"]

HEADLESS = cfg.getboolean("HEADLESS", fallback=True)
TIMEOUT = cfg.getint("TIMEOUT", fallback=10000)

LOG_PATH = cfg.get("LOG_PATH", "logs")
SCREENSHOT_PATH = cfg.get("SCREENSHOT_PATH", "screenshots")
SCREENSHOT_MODE = cfg.get("SCREENSHOT_MODE", "ERROR").upper()