from configparser import ConfigParser

config = ConfigParser()
config.read("monitor.ini", encoding="utf-8")

monitor = config["MONITOR"]

MAX_APPS = monitor.getint("MAX_APPS", fallback=0)
ORDER = monitor.get("ORDER", "ASC").upper()
ONLY_ENABLED = monitor.getboolean("ONLY_ENABLED", fallback=True)

SCREENSHOT_MODE = config["SCREENSHOT"].get(
    "MODE",
    fallback="ERROR"
).upper()

FILTROS = {}

if config.has_section("FILTROS"):

    for nome, valor in config.items("FILTROS"):

        FILTROS[nome] = valor.lower() == "true"