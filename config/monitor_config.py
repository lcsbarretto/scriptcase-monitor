from configparser import ConfigParser
from pathlib import Path
from utils.paths import CONFIG_DIR


config = ConfigParser()
config.optionxform = str
config.read(CONFIG_DIR / "monitor.ini", encoding="utf-8")

monitor = config["MONITOR"]

MAX_APPS = monitor.getint("MAX_APPS", fallback=0)
ORDER = monitor.get("ORDER", "ASC").upper()
ONLY_ENABLED = monitor.getboolean("ONLY_ENABLED", fallback=True)

SCREENSHOT_MODE = config.get(
    "SCREENSHOT",
    "MODE",
    fallback="ERROR"
).upper()

FILTROS = {}

if config.has_section("FILTROS"):
    for nome, valor in config.items("FILTROS"):
        FILTROS[nome] = valor.lower() == "true"