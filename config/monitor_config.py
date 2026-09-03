from configparser import ConfigParser
from pathlib import Path
from utils.paths import CONFIG_DIR

BASE_DIR = Path(__file__).resolve().parent

CONFIG_FILE = BASE_DIR / "monitor.ini"


def carregar_configuracao():

    config = ConfigParser()

    config.read(
        CONFIG_FILE,
        encoding="utf-8"
    )

    monitor = config["MONITOR"]

    max_apps = monitor.getint(
        "MAX_APPS",
        fallback=0
    )

    order = monitor.get(
        "ORDER",
        "ASC"
    ).upper()

    only_enabled = monitor.getboolean(
        "ONLY_ENABLED",
        fallback=True
    )

    filtros = {}

    if config.has_section("FILTROS"):

        for nome, valor in config.items(
            "FILTROS"
        ):

            filtros[nome] = (
                valor.lower() == "true"
            )

    screenshot_mode = "ERROR"

    if config.has_section("SCREENSHOT"):

        screenshot_mode = config["SCREENSHOT"].get(
            "MODE",
            "ERROR"
        ).upper()

    return {
        "MAX_APPS": max_apps,
        "ORDER": order,
        "ONLY_ENABLED": only_enabled,
        "FILTROS": filtros,
        "SCREENSHOT_MODE": screenshot_mode
    }


_config = carregar_configuracao()

MAX_APPS = _config["MAX_APPS"]
ORDER = _config["ORDER"]
ONLY_ENABLED = _config["ONLY_ENABLED"]
FILTROS = _config["FILTROS"]
SCREENSHOT_MODE = _config["SCREENSHOT_MODE"]